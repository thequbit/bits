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
            <a href="/projects">Projects</a>
             >
            <a href="/project?project_id=${project['id']}">${project['name']}</a>
             > New Ticket
            <div class="right top-links">
                <a href="/projectsettings?project_id=${project['id']}">Settings</a>
                <a href="/usersettings">${user.first} ${user.last}</a>
                
            </div>
        </div>
    </div>

    <div class="row">
        <div class="medium-8 columns">
            <div class="container-inner box shadow">
                <h5>New Ticket</h5>
                <input type="text" id="ticket-title" placeholder="ticket title"></text>
                <textarea id="ticket-contents" placeholder="markdown supported"></textarea>
                Ticket Assigned to: <a id="assigned-name" aria-expanded="false" href="#" data-dropdown="assigned-drop">Assign Ticket</a>
                <ul id="assigned-drop" class="f-dropdown" data-dropdown-content aria-hidden="true" tabindex="-1" data-options="is_hover:true">
                    % for assigned_user in assigned_users:
                        <li><a href="#" user_id="${assigned_user['user_id']}" user_name="${assigned_user['user']}">${assigned_user['user']}</a></li>
                    % endfor
                </ul>
            </div>
            <br/>
            <div id="submit-button-container">
                <a href="#" id="submit-ticket" class="small radius button">Submit</a>
            </div>
        </div>
        <div class="medium-4 columns">
            <div class="box shadow">
                <div class="box-title">
                    Existing Tickets
                    <div class="right">
                        <a href="/newticket?project_id=${project['id']}">New</a>
                    </div>
                </div>
                % if not tickets:
                    <div class="indent">
                        <div class="small-light-text">No tickets for this project.</div>
                    </div>
                % else:
                    % for ticket in tickets:
                        <div class="box-inner-container">
                            <a href="/ticket?ticket_id=${ticket['id']}">${ticket['title']}</a>
                            <div class="short-line-height extra-small-light-text">#${ticket['number']} opened by ${ticket['owner']} on ${ticket['created']}</div>
                        </div>
                    % endfor
                % endif
            </div> 
        </div>
    </div>

    <script>

        $('#submit-ticket').on('click', function(e) {

            show_loading("submitting ticket ...");

            var token = document.cookie.split('=')[1];
            var url = '/create_ticket.json';
            var project_id = ${project['id']}
            var title = $('#ticket-title').val();
            var contents = $('#ticket-contents').val();

            if ( title.trim() == '' ) {
                alert('A ticket at least needs a title.  Please supply a title for the ticket before trying to create it.')
                return;
            }

            $('#submit-button-container').html('Please wait ...');

            $.ajax({
                dataType: 'json',
                type: 'POST',
                data: {
                    project_id : project_id,
                    title : title,
                    contents : contents,
                    assigned_user_id : assigned_user_id
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

        var assigned_user_id = '';
        
        $(document).ready(function() {
        
            $('#assigned-drop').on('click', function(e) {
                assigned_user_id = $(e.target).attr('user_id');
                assigned_user_name = $(e.target).attr('user_name');
                $('#assigned-name').html(assigned_user_name);
                
                $('#assigned-drop').removeClass('open');
                $('#assigned-drop').css('left', '-99999px');
            });
        
            
        });

    </script>
