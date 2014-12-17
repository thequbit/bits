<%inherit file="base.mak"/>

    <div class="row">
        <div class="large-12 columns bottom-border">
            <a href="/">Home</a>
             > 
            <a href="/projects">Projects</a>
             >
            <a href="/project?project_id=${project['id']}">${project['name']}</a>
             > 
            <a href="/opentickets?project_id=${project['id']}">Tickets</a>
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
                    % if ticket['author_id'] == user.id:
                        % if ticket['closed'] == False:
                            <small>
                                <a href="#" id="edit-ticket-title">edit</a>
                            </small>
                        % endif
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
                                % if ticket['author_id'] == user.id:
                                    <div class="edit-link">
                                        <br/>
                                        <div class="right small-text">
                                            <a href="#" id="edit-ticket-contents">edit</a>
                                        </div>
                                    </div>
                                % endif
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
                        <a id="assigned-name" aria-expanded="false" href="#" data-dropdown="assigned-drop">Assign Ticket</a>
                    </div>
                    <ul id="assigned-drop" class="f-dropdown" data-dropdown-content aria-hidden="true" tabindex="-1" data-options="is_hover:true">
                        <li><a class="unassign-ticket-link" href="#" user_email="" user_name="">Unassign Ticket</a></li>
                    % for assigned_user in assigned_users:
                        <li><a class="assign-ticket-link" href="#" user_email="${assigned_user['email']}" user_name="${assigned_user['user']}">${assigned_user['user']}</a></li>
                    % endfor
                    </ul>
                    
                </div>           
 
                <h5>Comments</h5>

                % if not comments:
                    <div class="indent small-light-text">There are no comments yet for this ticket</div>
                % else:
                    % for comment in comments:
                        <div class="comment-container box shadow">
                            <div class="small-light-text">
                                On ${comment['created']} <a href="/user?user_id=${comment['owner_id']}">${comment['owner']}</a> wrote:
                            </div>
                            <div class="container-inner">
                                <div id="edit-comment-wrapper-${comment['id']}" style="display: none;">
                                    <textarea id="new-comment-contents-${comment['id']}">${comment['raw_contents'] | h}</textarea>
                                    <a href="#" comment_id="${comment['id']}" class="small radius button submit-comment-update">Submit</a>
                                </div>
                                <div id="comment-contents-${comment['id']}" class="comment-contents">
                                    ${comment['contents'] | n}
                                    % if comment['owner_id'] == user.id:
                                        <div class="edit-link">
                                            <div class="right small-text">
                                                <a href="#" comment_id="${comment['id']}" class="edit-comment-contents">edit</a>
                                            </div>
                                        </div>
                                        <div style="height: 10px;"></div>
                                    % endif
                                </div>
                            </div>
                            
                        </div>
                    % endfor
                % endif
                <br/>

                <div>
                    <label>Add Comment</label>
                    <textarea id="comment-contents" placeholder="markdown supported"></textarea>
                    <a href="#" id="submit-comment" class="small radius button">Submit</a>
                    % if ticket['closed'] == False:
                        <div class="right">
                            <a href="#" id="submit-comment-and-close" class="small radius button">Submit and Close</a>
                        </div>
                    % else:
                        <div class="right">
                            <a href="#" id="reopen-ticket" class="small radius button">Reopen Ticket</a>
                        </div>
                    % endif
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
    
    <style>
    
        
    
    </style>
    
    <script>

        function submit_comment(close, reopen) {
        
            console.log('submitting comment.');
        
            show_loading();
        
            var url = '/create_ticket_comment.json';
            var ticket_id = ${ticket['id']}
            var contents = $('#comment-contents').val();
            
            if ( close == true && contents.trim() == '' ) {
                contents = 'Closed.';
            } else if ( reopen == false && contents.trim() == '' ) {
                console.log('bad submit');
                return;
            }

            console.log('making ajax call');

            $.ajax({
                dataType: 'json',
                type: 'POST',
                data: {
                    ticket_id : ticket_id,
                    contents : contents,
                    close: close,
                    reopen: reopen,
                },
                url: url,
                success: function(data) {
                    if( data.success == true ) {
                        console.log('SUCCESS!');
                        window.location.href="/ticket?ticket_id=${ticket['id']}";
                    }
                },
                error: function(data) {
                    console.log('an error happened while creating ticket ...');
                    console.log(data)
                    // TODO: report error
                }
            });
        }

        function assign_user(email, unassign) {

            console.log('sending comment')

            //$('#submit-button-container').html('Please wait ...');

            show_loading();

            //var token = document.cookie.split('=')[1];
            var url = '/assign_user_to_ticket.json';
            var ticket_id = ${ticket['id']};
            
            $.ajax({
                dataType: 'json',
                type: 'POST',
                data: {
                    ticket_id: ticket_id,
                    email: email,
                    unassign: unassign,
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

            show_loading();

            var ticket_id = ${ticket['id']};
            var contents = $('#new-ticket-contents').val();
            var url = "/update_ticket_contents.json";

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

            show_loading();

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

        function update_comment_contents( comment_id ) {
            
            //show_loading();
            
            var newcontents = $('#new-comment-contents-' + comment_id).val();
            var url = "/update_ticket_comment.json";
            
            $.ajax({
                dataType: 'json',
                type: 'POST',
                data: {
                    ticket_id: "${ticket['id']}",
                    comment_id: comment_id,
                    contents: newcontents,
                },
                url: url,
                success: function(data) {
                    if( data.success == true ) {
                        window.location.href="/ticket?ticket_id=${ticket['id']}";
                    }
                },
                error: function(data) {
                    console.log('an error happened while updating the ticket comment ...');
                    console.log(data)
                    // TODO: report error
                }
            
            });
            
        }
        
        
        
        $(document).ready( function() {
        
            $('#assigned-drop').on('click', function(e) {
                
                assigned_user_email = $(e.target).attr('user_email');
                
                assigned_user_name = $(e.target).attr('user_name');
                $('#assigned-name').html(assigned_user_name);
                
                $('#assigned-drop').removeClass('open');
                $('#assigned-drop').css('left', '-99999px');
                
                //$('#assigned-container').html('Please wait ...');
                
                console.log('user email: ' + assigned_user_email);
                
                var unassign = false;
                if ( assigned_user_email == '' ) {
                    unassign = true;
                }
                
                //console.log('unassigned: ' + unassign );
                
                assign_user(assigned_user_email, unassign);
                
                return false;
            });
        
            $('#submit-comment').on('click', function(e) {
                submit_comment(false, false);
                
                return false;
            });
            
            $('#submit-comment-and-close').on('click', function(e) {
                submit_comment(true, false);
                
                return false;
            });
            
            $('#reopen-ticket').on('click', function(e) {
                submit_comment(false, true);
                
                return false;
            });
            
            /*
            $('submit-comment-update').on('click', function(e) {
                
                var comment_id = e.target.getAttribute('comment_id');
                
                submit_comment_update(comment_id);
                
            });
            */

            $('#edit-ticket-contents').on('click', function(e) {

                var html = '';
                
                $('#ticket-contents').hide();
                $('#edit-ticket-wrapper').show();

                //$('#ticket-contents-wrapper').html(html);
                $('#submit-ticket').on('click', function(ee) {
                
                    update_ticket_contents();

                    return false;

                });
                
                return false;

            });

            $('#edit-ticket-title').on('click', function(e) {
            
                $('#ticket-title').hide();
                $('#edit-ticket-title-wrapper').show();

                $('#submit-ticket-title').on('click', function(ee) {
                
                    update_ticket_title();
                
                    return false;
                
                });
 
                return false;
 
            });
            
            $('a.edit-comment-contents').on('click', function(e) {
                
                var comment_id = e.target.getAttribute('comment_id');
                
                $('#comment-contents-' + comment_id).hide();
                $('#edit-comment-wrapper-' + comment_id).show();
                
                $('a.submit-comment-update').on('click', function(e) {
                
                    var innercomment_id = e.target.getAttribute('comment_id');
                
                    update_comment_contents( innercomment_id );
                    
                    return false;
                    
                });
                
                return false;
            });
        
        });

    </script>
