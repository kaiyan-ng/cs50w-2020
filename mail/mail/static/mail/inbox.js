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
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
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
        const background = email.read ? 'bg-light' : 'bg-white';
        email_div.classList.add(background);

        // Construct inner HTML for the email div
        email_div.innerHTML = `
        <div class="container">
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

        // Append the email div to the emails view
        emails_div.append(email_div);

      })
  })
  .catch(error => {
    console.error('Error fetching emails:', error);
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