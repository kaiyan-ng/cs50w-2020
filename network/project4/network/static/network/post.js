document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.edit-post').forEach(button =>{
        button.addEventListener('click', event =>{
            event.preventDefault();
            const post_id = button.dataset.postId;
            edit(post_id);
        })
    })

    document.querySelectorAll('.like-post').forEach(button => {
        button.addEventListener('click', event => {
            event.preventDefault();
            console.log('Like button clicked');
            const post_id = button.dataset.postId;
            console.log('Post liked: ', post_id);
            like(post_id);
        })
    })

    document.querySelectorAll('i').forEach(like => {
        const post_id = like.parentNode.getAttribute('data-post-id');
        load_likes(post_id);
    })
    

    
})

function load_likes(post_id) {
    fetch(`/like/${post_id}`)
        .then(response => {
            if (response.ok) {
                // Parse the response as JSON
                return response.json();
            } else {
                throw new Error('Failed to load likes');
            }
        })
        .then(data => {
            const likeIcon = document.querySelector(`#like-${post_id}`);
            if (likeIcon) {
                if (data.liked) {
                    // User has liked the post, update icon to filled heart
                    likeIcon.classList.remove('fa-heart-o');
                    likeIcon.classList.add('fa-heart');
                } else {
                    // User has not liked the post, update icon to empty heart
                    likeIcon.classList.remove('fa-heart');
                    likeIcon.classList.add('fa-heart-o');
                }
            }
        })
        .catch(error => {
            console.error('Error loading likes:', error);
        });
}

function edit(id){
    fetch(`/posts/${id}`)
    .then(response => response.json())
    .then(post => {

        //Preserve line breaks in post content
        post.content = post.content.replace(/\n/g, '<br>'); 

        const display_format = document.querySelector(`#post-${post.id}`).innerHTML;

        document.querySelector(`#post-${post.id}`).innerHTML = `
        <textarea rows="3" style="width: 100%;" id="post_${post.id}">${post.content}</textarea>
        <button class="btn btn-primary" id="save-post">Save</button> 
        `

        document.querySelector('#save-post').addEventListener('click', event => {
            event.preventDefault();
            const new_content = document.querySelector(`#post_${post.id}`).value;
            save_changes(post.id, new_content, display_format);
        })
    })
    .catch(error => {
        console.error('Error fetching post:', error);
    });
}

function save_changes(id, new_content, display_format){
    fetch(`/posts/${id}`, {
        method: 'PUT', 
        body: JSON.stringify({
            content: new_content
        })
    })
    .then(response => {
        // Check if the response status is 204 (No Content)
        if (response.status === 204) {
          // If successful, display post with new content
          document.querySelector(`#post-${id}`).innerHTML = display_format;
          location.reload();
        } else {
          // If not 204, parse the response as JSON and log the result
          return response.json().then(result => {
            console.log(result);
          });
        }
      })
      .catch(error => {
        console.error('Error saving post:', error);
      });
}

function like(post_id){
    fetch(`/like/${post_id}`, {
        method: 'PUT'
    })
    .then(response => {
        if (response.status === 204) {
            location.reload();
        } else {
            // If not 204, parse the response as JSON and log the result
            return response.json().then(result => {
              console.log(result);
            });
          }
    })
    .catch(error => {
        console.error('Error liking/unliking post:', error);
    });
}