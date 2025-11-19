# Dynamic Instructions for Creating a LinkedIn Post

This document outlines the dynamic steps to create and publish a LinkedIn post using the Gemini CLI and browser automation tools.

## 1. Navigate to LinkedIn Feed

Ensure you are on the LinkedIn feed page. If not, navigate to `https://www.linkedin.com/feed/`.

## 2. Initiate Post Creation

- Use `browser_snapshot()` to get the current state of the page.
- Identify the `ref` for the "Start a post" button.
- Use `browser_click(ref="<ref_of_start_a_post_button>")` to open the post creation dialog.

## 3. Get Post Idea from User

- Ask the user for the topic or idea for the post. For example: "What would you like to post about?"

## 4. Generate Post Content

- Based on the user's input, generate a draft of the post content. This should include:
    - A catchy title/headline.
    - The body of the post.
    - Relevant hashtags.

## 5. User Review and Modification

- Present the generated content to the user.
- Ask the user if they would like to modify the content. For example: "Here is a draft of the post. Would you like to make any changes?"

## 6. Incorporate User Changes

- If the user wants to modify the post, ask them to provide the complete, updated content.
- Use `browser_type(ref="<ref_of_text_editor>", text="<updated_content>")` to fill the text editor with the new content.

## 7. Final Permission

- After the content is finalized and entered, ask the user for final permission before publishing. For example: "I have entered the content into the LinkedIn post creator. Please confirm if you would like me to proceed with publishing this post."

## 8. Publish the Post

- Once the user gives final permission:
    - Use `browser_snapshot()` to get the current `ref` for the "Post" button.
    - Use `browser_click(ref="<ref_of_post_button>")` to publish the post.

## 9. Confirm Post Success

- After clicking "Post", check for a confirmation message like "Post successful."
- Inform the user that the post has been successfully published.
