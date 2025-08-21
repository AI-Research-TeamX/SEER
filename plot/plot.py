import json
import matplotlib.pyplot as plt
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import matplotlib.patches as patches
from collections import defaultdict
import plotly.graph_objects as go
from sklearn.manifold import TSNE
from itertools import cycle
import re

os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def plot_sim_score(filename):
    with open(filename) as f:
        data = json.load(f)
    
    model = SentenceTransformer("XXX/models/bge-large-en-v1.5")
    for d in data:
        d["embedding"] = model.encode(d["question"], normalize_embeddings=True)
    print(data[0]["embedding"].shape)

    # Calculate cosine similarity
    n = len(data)
    embeddings = np.stack([d["embedding"] for d in data])
    sim_matrix = embeddings @ embeddings.T


    # Sort data by class to group similar questions together
    sorted_data = sorted(enumerate(data), key=lambda x: x[1]["class"])
    sorted_indices = [i for i, _ in sorted_data]
    sorted_sim_matrix = sim_matrix[np.ix_(sorted_indices, sorted_indices)]
    sorted_classes = [d["class"] for _, d in sorted_data]

    # Find boundaries for each class
    class_boundaries = defaultdict(list)
    for idx, cls in enumerate(sorted_classes):
        class_boundaries[cls].append(idx)

    plt.figure()
    plt.imshow(sorted_sim_matrix, interpolation="nearest", cmap="viridis")
    plt.colorbar()
    plt.xticks([])
    plt.yticks([])

    ax = plt.gca()
    for cls, indices in class_boundaries.items():
        start = indices[0]
        end = indices[-1]
        width = end - start + 1
        rect = patches.Rectangle(
            (start - 0.5, start - 0.5),
            width, width,
            linewidth=1, edgecolor='red', facecolor='none'
        )
        ax.add_patch(rect)

    plt.tight_layout()
    os.makedirs("plot", exist_ok=True)
    plt.savefig("plot/similarity_matrix.pdf")
    plt.close()

    # Optional: update HTML plot with rectangles
    questions = [f"Q{i}: ({d['class']}){d['question']}" for i, d in sorted_data]

    # Create heatmap
    fig = go.Figure(
        data=go.Heatmap(
            z=sorted_sim_matrix,
            x=questions,
            y=questions,
            colorscale="Viridis",
            hoverinfo="z+x+y",
        )
    )

    # Add red rectangles for class boundaries
    shape_list = []
    for cls, indices in class_boundaries.items():
        start = indices[0] - 0.5
        end = indices[-1] + 0.5
        shape_list.append(
            dict(
                type="rect",
                xref="x",
                yref="y",
                x0=start,
                y0=start,
                x1=end,
                y1=end,
                line=dict(color="red", width=2),
                fillcolor="rgba(0,0,0,0)",  # Transparent fill
                layer="above"
            )
        )

    fig.update_layout(
        title="Cosine Similarity Matrix with Class Boundaries",
        xaxis_title="Questions",
        yaxis_title="Questions",
        width=1000,
        height=1000,
        xaxis=dict(showticklabels=False, constrain="domain"),
        yaxis=dict(showticklabels=False, constrain="domain"),
        shapes=shape_list
    )

    fig.write_html("plot/similarity_matrix.html")


def plot_2d(filename):
    # Load data
    with open(filename) as f:
        data = json.load(f)

    # Load model and compute embeddings
    model = SentenceTransformer("XXX/models/bge-large-en-v1.5")
    for d in data:
        d["embedding"] = model.encode(d["question"], normalize_embeddings=True)
    print("Embedding shape:", data[0]["embedding"].shape)

    # Stack embeddings
    embeddings = np.stack([d["embedding"] for d in data])

    # Run t-SNE
    tsne = TSNE(n_components=2, perplexity=50, n_iter=1000, random_state=42)
    tsne_results = tsne.fit_transform(embeddings)
    print("t-SNE result shape:", tsne_results.shape)

    # Collect unique classes and assign colors
    classes = sorted(set(d["class"] for d in data))
    color_cycle = cycle(plt.rcParams["axes.prop_cycle"].by_key()["color"])
    class_to_color = {cls: next(color_cycle) for cls in classes}

    # Matplotlib static plot
    plt.figure(figsize=(10, 10))
    for cls in classes:
        indices = [i for i, d in enumerate(data) if d["class"] == cls]
        x = tsne_results[indices, 0]
        y = tsne_results[indices, 1]
        plt.scatter(x, y, label=cls, color=class_to_color[cls], alpha=0.6)

    plt.title("t-SNE of Question Embeddings by Class")
    plt.legend()
    plt.tight_layout()
    os.makedirs("plot", exist_ok=True)
    plt.savefig("plot/2d_plot.pdf")
    plt.close()

    # Plotly interactive plot
    fig = go.Figure()
    for cls in classes:
        indices = [i for i, d in enumerate(data) if d["class"] == cls]
        x = tsne_results[indices, 0]
        y = tsne_results[indices, 1]
        text = [f"Q{i}: ({data[i]['class']}) {data[i]['question']}" for i in indices]

        fig.add_trace(go.Scatter(
            x=x,
            y=y,
            mode="markers",
            name=cls,
            text=text,
            marker=dict(size=6, opacity=0.7),
            hoverinfo="text"
        ))

    fig.update_layout(
        title="t-SNE of Question Embeddings by Class",
        width=1000,
        height=1000,
    )
    fig.write_html("plot/2d_plot.html")


def plot_correlation(filename):
    with open(filename) as f:
        raw_data = f.read()
    
    questions = re.findall(r"==========Question:\s*(.*?)\s*,\s*GT:", raw_data, re.DOTALL)
    print(f"Matched {len(questions)} questions")
    
    examples = re.findall(r"OUTPUT: selected examples: \n(.*?)----SELECT_DEBUGGING_END----", raw_data, re.DOTALL)
    examples = [re.findall(r"-- Question: (.*?); tools: ", ex, re.DOTALL) for ex in examples]
    print(f"Matched {len(examples)} examples")
    
    eval_results = re.findall(r"==========LLM_Evaluate_(.*?)==========", raw_data, re.DOTALL)
    eval_results = [True if res == "Correct" else False for res in eval_results]
    print(f"Matched {len(eval_results)} eval results, {sum(eval_results)} correct, {len(eval_results) - sum(eval_results)} incorrect")

    summary = raw_data.split("LLM evaluator: ")[-1].split("=")[0].split("/")
    print(f"Summary eval results: {summary}")
    summary = [int(s) for s in summary if s.isdigit()]

    assert len(questions) == len(examples) == len(eval_results) == summary[1], "Questions and examples count mismatch"
    assert sum(eval_results) == summary[0], "Correct count mismatch"
    
    model = SentenceTransformer("XXX/models/bge-large-en-v1.5")
    data = []
    for q, ex, res in zip(questions, examples, eval_results):
        embed_q = model.encode(q, normalize_embeddings=True)
        embed_ex = model.encode(ex, normalize_embeddings=True)
        similarity = embed_q @ embed_ex.T
        similarity = np.mean(similarity)
        theta = np.arccos(similarity)
        data.append(
            {
                "question": q,
                "examples": ex,
                "similarity": similarity,
                "reward": 1 if res else 0.5,
                "theta": theta
            }
        )
    
    # Plot correlation between similarity and reward
    plt.figure(figsize=(10, 10))
    ax = plt.subplot(111, polar=True)

    sc = ax.scatter(
        [d["theta"] for d in data],
        [d["reward"] for d in data],
        c=[d["similarity"] for d in data],
        cmap="viridis",
        alpha=0.6,
        edgecolors="k",
        linewidth=0.5
    )

    # ax.set_title("Correlation between Similarity and Reward")
    # plt.colorbar(sc, ax=ax, label="Cosine Similarity")
    ax.set_thetamin(0)
    ax.set_thetamax(90)
    ax.set_rticks([0.5, 1.0])
    ax.set_yticklabels(["Incorrect", "Correct"])

    plt.tight_layout()
    os.makedirs("plot", exist_ok=True)
    plt.savefig("plot/correlation_plot.pdf")
    plt.close()
