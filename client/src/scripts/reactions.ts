async function handleReaction(songId: string, action: string, userId: string): Promise<void> {
  try {

    // Update button states
    const container = document.querySelector(
      `.reaction-buttons[data-song-id="${songId}"]`
    ) as HTMLElement;

    if (!container) {
        console.log("couldnt find container");
        return;
    }

    const likeBtn = container.querySelector('[data-action="like"]') as HTMLButtonElement;
    const dislikeBtn = container.querySelector('[data-action="dislike"]') as HTMLButtonElement;

    if (action === "like") {
      if (likeBtn.classList.contains('like-active-button')) { // like button is already selected
        likeBtn.classList.add('neutral-active-button');
        likeBtn.classList.remove('like-active-button');
        action = 'unlike';
      }
      else {
        likeBtn.classList.add("like-active-button");
        likeBtn.classList.remove("neutral-active-button");
        dislikeBtn.classList.remove("dislike-active-button");
        dislikeBtn.classList.add("neutral-active-button");
      }
    } else if (action === "dislike") {
      if (dislikeBtn.classList.contains('dislike-active-button')) { // dislike button is already selected
        dislikeBtn.classList.add('neutral-active-button');
        dislikeBtn.classList.remove('dislike-active-button');
        action = 'undislike';
      }
      else {
        dislikeBtn.classList.add("dislike-active-button");
        dislikeBtn.classList.remove("neutral-active-button");
        likeBtn.classList.remove("like-active-button");
        likeBtn.classList.add("neutral-active-button");
      }
    }

    console.log("✅ Reaction updated visually");

    console.log("Sending reaction with:", { songId, action, userId });

    const res = await fetch("/react", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ songId, action, userId })
    });

    if (!res.ok) {
      const error = await res.json();
      console.error("❌ Reaction failed:", error);
      return;
    }

  } catch (err) {
    console.error("❌ Error sending reaction:", err);
  }
}
(window as any).handleReaction = handleReaction;
