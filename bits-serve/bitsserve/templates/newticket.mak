<%inherit file="base.mak"/>

    <style>
 
    </style>
    
    <!--
    <div class="row">
        <div class="large-12 columns">
            <a href="/">Back to Project</a>
        </div>
    </div> 
    -->

    <div class="row">
        <div class="medium-12 columns bottom-border">
            <a href="/">Home</a>
             >
            <a href="/project?project_id=${project['id']}">${project['name']}</a>
             > New Ticket
            <div class="right top-links">
                <a href="/prjectsettings?project_id=${project['id']}">Settings</a>
                <<a href="/usersettings">${user.first} ${user.last}</a>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="medium-8 columns">
            <div class="container-inner box shadow">
                <h5>New Ticket<h5>
                <input type="text" id="ticket-title" placeholder="ticket title"></text>
                <textarea id="ticket-contents" placeholder="markdown supported"></textarea>
            </div>
            <br/>
            <a href="#" id="submit-ticket" class="small radius button">Submit</a>
        </div>
        <div class="medium-4 columns">
            <div class="box shadow">
                <div class="box-title">
                    Existing Tickets
                    <!--<div class="right">
                        <a href="/newticket?project_id=${project['id']}">New</a>
                    </div>-->
                </div>
                % if not tickets:
                    <div class="indent">
                        <div class="small-light-text">No tickets for this project.</div>
                    </div>
                % else:
                    % for ticket in tickets:
                        <div class="box-inner-container">
                            <a href="/ticket?ticket_id=${ticket['id']}">${ticket['title']}</a>
                            <div class="short-line-height extra-small-light-text"> opened by ${ticket['owner']} on ${ticket['created']}</div>
                        </div>
                    % endfor
                % endif
            </div> 
        </div>
    </div>

    <script>

        $('#submit-ticket').on('click', function(e) {

            console.log('sending comment')

            var token = document.cookie.split('=')[1];
            var url = '/create_ticket.json';
            var project_id = ${project['id']}
            var title = $('#ticket-title').val();
            var contents = $('#ticket-contents').val();

            $.ajax({
                dataType: 'json',
                type: 'POST',
                data: {
                    project_id : project_id,
                    title : title,
                    contents : contents
                },
                url: url,
                success: function(data) {
                    if( data.success == true ) {
                        console.log('SUCCESS!');
                        window.location.href="/ticket?ticket_id=" + data.ticket_id;
                    }
                },
                error: function(data) {
                    console.log('an error happened while creating ticket ...');
                    // TODO: report error
                }
            });

        });

        // TODO: hook up submit and close button

    </script>
