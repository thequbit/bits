<%inherit file="base.mak"/>

    <div class="row">
        <div class="large-12 columns bottom-border">
            <a href="/">Home</a>
             > 
            <a href="/project?project_id=${project['id']}">${project['name']}</a>
             > 
            <a href="/tickets?project_id=${project['id']}">Tickets</a>
             > Ticket
            <div class="right top-links">
                <a href="/projectsettings?project_id=${project['id']}">Settings</a>
                <a href="/usersettings">${user.first} ${user.last}</a>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="medium-12 column">
            <div class="page-title">
                <div class="right manage-link">
                    <a href="/manageproject?project_id=${project['id']}">Manage Project</a>
                </div>
                <div id="ticket-title">
                    <h4>Ticket #${ticket['number']} : ${ticket['title']}
                    % if ticket['closed'] == False:
                        <small>
                            <a href="#" id="edit-ticket-title">edit</a>
                        </small>
                    % endif
                    </h4>
                    % if ticket['closed'] == True:
                        <h4 class="closed-label">[CLOSED]</h4>
                    % endif
                </div>
            </div>
        </div>
    </div>

    <br/><br/>



    <div class="row">
        <div class="medium-8 columns">
            <div class="ticket-container">
                <div id="ticket-title-wrapper">
                    <div>
                        <div id="edit-ticket-title-wrapper" style="display: none">
                            <br/>
                            <input type="text" id="new-ticket-title" value="${ticket['title'] | h}" style="font-weight: bold; width: 100%;"></input>
                            <a href="#" id="submit-ticket-title" class="small radius button">Submit</a>
                        </div>
                    </div>
                </div>
                
                <div class="small-light-text">
                    Opened by ${ticket['owner']} on ${ticket['created']}
                </div>
               
                <div class="indent indent-right">
                    <div class="box shadow">
                        <div class="container-inner">
                            <div id="edit-ticket-wrapper" style="display: none;">
                                <textarea id="new-ticket-contents">${ticket['raw_contents'] | h}</textarea>
                                <a href="#" id="submit-ticket" class="small radius button">Submit</a>
                            </div>
                            <div id="ticket-contents">
                                ${ticket['contents'] | n}
                                <div class="edit-link">
                                    <br/>
                                    <div class="right small-text">
                                        <a href="#" id="edit-ticket-contents">edit</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                </br>
                <div id="assigned-container">
                     
                    % if ticket['assigned_id'] != None:
                        Assigned: <a href="/user?user_id=${ticket['assigned_id']}">${ticket['assigned_user']}</a>
                        <br/>
                    % endif
                    <div class="small-light-text">
                        <a id="assigned-name" aria-expanded="false" href="#" data-dropdown="assigned-drop">re-assign Ticket</a>
                    </div>
                    <ul id="assigned-drop" class="f-dropdown" data-dropdown-content aria-hidden="true" tabindex="-1" data-options="is_hover:true">
                    % for assigned_user in assigned_users:
                        <li><a href="#" user_email="${assigned_user['email']}" user_name="${assigned_user['user']}">${assigned_user['user']}</a></li>
                    % endfor
                    </ul>
                    
                </div>
                <br/>           
 
                <h5>Comments</h5>            

                % if not comments:
                    <div class="indent small-light-text">There are no comments yet for this ticket</div>
                % else:
                    % for comment in comments:
                        <div class="comment-containeri box shadow">
                            <div class="small-light-text">
                                On ${comment['created']} <a href="/user?user_id=${comment['owner_id']}">${comment['owner']}</a> wrote:
                            </div>
                            <div class="container-inner">
                                ${comment['contents'] | n}
                            </div>
                        </div>
                    % endfor
                % endif
                <br/>

                <div>
                    <label>Add Comment</label>
                    <textarea id="comment-contents" placeholder="markdown supported"></textarea>
                    <a href="#" id="submit-comment" class="small radius button">Submit</a>
                    <div class="right">
                        <a href="#" id="submit-comment-and-close" class="small radius button">Submit and Close</a>
                    </div>
                </div>
            </div>

        </div>
        <div class="medium-4 columns">
            <div class="box shadow">
                <div class="box-title">
                    Existing Tickets
                    <div class="right">
                        <a href="/newticket?project_id=${project['id']}">New Ticket</a>
                    </div>
                </div>
                % if not tickets:
                    <div class="indent">
                        <div class="small-light-text">No tickets for this project.</div>
                    </div>
                % else:
                    % for existing_ticket in tickets:
                        <div class="box-inner-container">
                            <a href="/ticket?ticket_id=${existing_ticket['id']}">${existing_ticket['title']}</a>
                            <div class="short-line-height extra-small-light-text"> opened by ${existing_ticket['owner']} on ${existing_ticket['created']}</div>
                        </div>
                    % endfor
                % endif
            </div>
            <hr/>
        </div> 
    </div>
    
    
    <script>

        function submit_comment(callback) {
        
            //var token = document.cookie.split('=')[1]; 
            var url = '/create_ticket_comment.json';
            var ticket_id = ${ticket['id']}
            //var author_id = localStorage.getItem("user_id")
            //var project_id = ${project['id']};
            var contents = $('#comment-contents').val();
            
            if ( contents.trim() == '' ) {
                //alert('Please make sure there is contents to our comment before submitting.');
                return;
            }

            $.ajax({
                dataType: 'json',
                type: 'POST',
                data: {
                    ticket_id : ticket_id,
                    //author_id : author_id,
                    //project_id : project_id,
                    contents : contents
                },
                url: url,
                success: function(data) {
                    if( data.success == true ) {
                        console.log('SUCCESS!');
                        window.location.href="/ticket?ticket_id=${ticket['id']}";
                        callback();
                    }
                },
                error: function(data) {
                    console.log('an error happened while creating ticket ...');
                    console.log(data)
                    // TODO: report error
                }
            });
        }

        function close_ticket() {
            
            //var token = document.cookie.split('=')[1]; 
            var url = '/close_ticket.json';
            var ticket_id = ${ticket['id']}
            
            $.ajax({
                dataType: 'json',
                type: 'POST',
                data: {
                    ticket_id : ticket_id,
                },
                url: url,
                success: function(data) {
                    if( data.success == true ) {
                        window.location.href="/ticket?ticket_id=${ticket['id']}";
                    }
                },
                error: function(data) {
                    console.log('an error happened while closing ticket ...');
                    console.log(data)
                    // TODO: report error
                }
            });
            
        }

        function assign_user(email) {

            console.log('sending comment')

            $('#submit-button-container').html('Please wait ...');

            //var token = document.cookie.split('=')[1];
            var url = '/assign_user_to_ticket.json';
            var ticket_id = ${ticket['id']};
            
            $.ajax({
                dataType: 'json',
                type: 'POST',
                data: {
                    ticket_id: ticket_id,
                    email: email,
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

        }

        function update_ticket_contents() {

            var ticket_id = ${ticket['id']};
            var contents = $('#new-ticket-contents').val();
            var url = "/update_ticket_contents.json?";

            $.ajax({
                dataType: 'json',
                type: 'POST',
                data: {
                    ticket_id : ticket_id,
                    contents : contents,
                },
                url: url,
                success: function(data) {
                    if( data.success == true ) {
                        window.location.href="/ticket?ticket_id=${ticket['id']}";
                    }
                },
                error: function(data) {
                    console.log('an error happened while closing ticket ...');
                    console.log(data)
                    // TODO: report error
                }
            });
        }

        function update_ticket_title() {

            var ticket_id = ${ticket['id']};
            var title = $('#new-ticket-title').val();
            var url = "/update_ticket_title.json?";

            $.ajax({
                dataType: 'json',
                type: 'POST',
                data: {
                    ticket_id : ticket_id,
                    title : title,
                },
                url: url,
                success: function(data) {
                    if( data.success == true ) {
                        window.location.href="/ticket?ticket_id=${ticket['id']}";
                    }
                },
                error: function(data) {
                    console.log('an error happened while closing ticket ...');
                    console.log(data)
                    // TODO: report error
                }
            });
        }

        //var assigned_user_id = '';
    
        $(document).ready( function() {
        
            $('#assigned-drop').on('click', function(e) {
                assigned_user_email = $(e.target).attr('user_email');
                assigned_user_name = $(e.target).attr('user_name');
                $('#assigned-name').html(assigned_user_name);
                
                $('#assigned-drop').removeClass('open');
                $('#assigned-drop').css('left', '-99999px');
                
                $('#assigned-container').html('Please wait ...');
                
                assign_user(assigned_user_email);
            });
        
            $('#submit-comment').on('click', function(e) {
                submit_comment();
            });
            
            $('#submit-comment-and-close').on('click', function(e) {
                close_ticket();
            });

            $('#edit-ticket-contents').on('click', function(e) {

                var html = '';
                //html += '<textarea id="new-ticket-contents"></textarea>';
                //html += '<div id="submit-button-container">'
                //html += '<a href="#" id="submit-ticket" class="small radius button">Submit</a>';
                //html += '</div>'

                $('#ticket-contents').hide();
                $('#edit-ticket-wrapper').show();

                //$('#ticket-contents-wrapper').html(html);
                $('#submit-ticket').on('click', function(ee) {
                
                    update_ticket_contents();

                });

            });

            $('#edit-ticket-title').on('click', function(e) {
            
                $('#ticket-title').hide();
                $('#edit-ticket-title-wrapper').show();

                $('#submit-ticket-title').on('click', function(ee) {
                
                    update_ticket_title();
                
                });
 
            });
        
        });

    </script>
