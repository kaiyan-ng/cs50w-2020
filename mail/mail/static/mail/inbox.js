document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // When compose mail form is submitted, send the mail
  document.querySelector('#compose-form').addEventListener('submit', event =>{
    event.preventDefault();
    send_email();
  })

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-content-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#email-content-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Query the API for latest emails in the mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      // ... do something else with emails ...

        // Display emails
        const emails_div = document.querySelector('#emails-view')
        emails.forEach(email => {
          // Create a div for each email
        const email_div = document.createElement('div');
        email_div.classList.add('border', 'border-dark', 'd-flex', 'p-2');

        // Set background color based on read status
        const background = email.read ? 'bg-white' : 'bg-light';
        email_div.classList.add(background);

        // Set id attribute for div as email's id
        //email_div.setAttribute('id', `${email.id}`)

        // Construct inner HTML for the email div
        email_div.innerHTML = `
        <div class="container ">
        <div class="row">
          <div class="col-md-auto">
            <b>${email.sender}</b>
          </div>
          <div class="col">
            ${email.subject}
          </div>
          <div class="col-3 text-right text-muted">
            ${email.timestamp}
          </div>
        </div>
        `;

        email_div.addEventListener('click', event => {
          load_email(email.id, mailbox)
        })
        // Append the email div to the emails view
        emails_div.append(email_div);

      })
  })
  .catch(error => {
    console.error('Error fetching emails:', error);
  });
}

function load_email(id, mailbox){

  // Show the email content and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-content-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Clear existing email content
  document.querySelector('#email-content-view').innerHTML = '';

  // Mark email as read
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  });

  // Load email content
   fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);

      // ... do something else with email ...
      
      //Preserve line breaks in email content
      email.body = email.body.replace(/\n/g, '<br>'); 

      // Display email content
      const content_div = document.createElement('div');
      content_div.innerHTML = `
      <div class="row">
      <div class="col">
          <p><b>From:</b> ${email.sender} </p>
      </div>
      ${mailbox !== 'sent' ? '<div class="col text-right"><button id="archive-email" class="btn btn-outline-primary">' + (email.archived ? 'Unarchive' : 'Archive') + '</button></div>' : ''}
      </div>
      <p><b>To:</b> ${email.recipients}</p>
      <p><b>Subject:</b> ${email.subject}</p>
      <p><b>Timestamp:</b> ${email.timestamp}</p>
      <button id="reply-email" class="btn btn-outline-primary">Reply</button>
      <hr>
      <p>${email.body}</p>
      `;
      document.querySelector('#email-content-view').append(content_div);

      // When archive/unarchive button is pressed
      const archive_button = document.querySelector('#archive-email')
      archive_button.addEventListener('click', event => {
        event.preventDefault();
        if (email.archived){
          unarchive_email(email.id);
        } else {
          archive_email(email.id);
        }
      });
    
      document.querySelector("#reply-email").addEventListener('click', event =>{
        event.preventDefault();
        reply_email(email);
      });
  })
  .catch(error => {
    console.error('Error fetching email:', error);
  });

}

function archive_email(id, archive) {
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      archived: !archive
    })
  })
  .then(response => {
    // Check if the response status is 204 (No Content)
    if (response.status === 204) {
      // If successful, directly load the inbox mailbox
      load_mailbox('inbox');
    } else {
      // If not 204, parse the response as JSON and log the result
      return response.json().then(result => {
        console.log(result);
        // Once email has been archived, load inbox mailbox
        load_mailbox('inbox');
      });
    }
  })
  .catch(error => {
    console.error('Error archiving email:', error);
  });
}

function unarchive_email(id){
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: false
    })
  })
  .then(response => {
    // Check if the response status is 204 (No Content)
    if (response.status === 204) {
      // If successful, directly load the inbox mailbox
      load_mailbox('inbox');
    } else {
      // If not 204, parse the response as JSON and log the result
      return response.json().then(result => {
        console.log(result);
        // Once email has been archived, load inbox mailbox
        load_mailbox('inbox');
      });
    }
  })
  .catch(error => {
    console.error('Error archiving email:', error);
  });
}


function send_email(){
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      //Once email has been sent, load sent mailbox
      load_mailbox('sent');
  });
}

function reply_email(email){
  compose_email();

  replied = email.subject.slice(0,3) === "Re:";
  // Prefill
  document.querySelector('#compose-recipients').value = `${email.sender}`;
  if (replied){
    document.querySelector('#compose-subject').value = `${email.subject}`;
  } else {
    document.querySelector('#compose-subject').value = 'Re: ' + `${email.subject}`;
  }
  document.querySelector('#compose-body').value = `
   On ${email.timestamp} ${email.sender} wrote:
   ${email.body}
  `;
}
