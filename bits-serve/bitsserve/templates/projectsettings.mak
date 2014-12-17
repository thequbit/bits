<%inherit file="base.mak"/>

    <style>
    
        div.assigned-contianer small {
            font-size: 75%;
            margin-left: 5px !important;
        }
    
    </style>
    
    <div class="row">
        <div class="medium-12 columns bottom-border">
            <a href="/">Home</a>
             >
            <a href="/projects">Projects</a>
             >
            <a href="/project?project_id=${project['id']}">${project['name']}</a>
             > Settings
            <div class="right top-links">
                <a href="/usersettings">${user.first} ${user.last}</a>
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="medium-12 columns">
            <h5>Project Settings</h5>
            </br>
            <a class="small button round">Save Settings</a>
        </div>
    </div>
    
    <div class="row">
        <div class="medium-4 columns">
            <div class="box shadow">
                <div class="bottom-border"><h5>General Settings</h5></div>
                <div class="box indent small-light-text">
                    Configure your project settings.
                </div>
                <div class="container-inner">
                    <div><input type="checkbox"></input>Enable Project</div>
                </div>
                <div class="box indent small-light-text">
                    Set a completion date for the project.  
                </div>
                <div class="container-inner">
                    <input type="text" placeholder="Due Date"></input>
                </div>
                <div class="box indent small-light-text">
                    Assign this project to a specific customer.
                </div>
                <div class="container-inner">
                    <input type="text" placeholder="Customer Name"></input>
                </div>
            </div>
            <hr/>
        </div>
        <div class="medium-4 columns">
            <div class="box shadow">
                <div class="bottom-border"><h5>Feature Settings</h5></div>
                <div class="box indent small-light-text">
                    Select the features that will be included on the project page for this project.
                </div>
                <div class="container-inner">
                    <div><input type="checkbox"></input>Tasks</div>
                    <div><input type="checkbox"></input>Tickets</div>
                    <div><input type="checkbox"></input>Lists</div>
                    <div><input type="checkbox"></input>Requirements</div>
                    <div><input type="checkbox"></input>Milestones</div>
                    <div><input type="checkbox"></input>Notes</div>
                </div>
            </div>
            <hr/>
        </div>
        <div class="medium-4 columns">
            <div class="box shadow">
                <div class="bottom-border"><h5>Participants</h5></div>
                <div class="box indent small-light-text">
                    Manage the users that have access to this project.
                </div>
                
                <div class="container-inner">
                    <a id="assigned-name" aria-expanded="false" href="#" data-dropdown="assigned-drop">Assign User to Project</a>
                    <div id="error-field" class="">
                        <br/>
                    </div>
                    <ul id="assigned-drop" class="f-dropdown" data-dropdown-content aria-hidden="true" tabindex="-1" data-options="is_hover:true">
                    % for organization_user in organization_users:
                        <li><a href="#" user_email="${organization_user.email}" user_name="${organization_user.first} ${organization_user.last}">${organization_user.first} ${organization_user.last}</a></li>
                    % endfor
                    </ul>
                </div>
                
                <div class="assigned-contianer">
                    <div class="container-inner">
                    Currently Assigned:
                    % for assigned_user in assigned_users:
                        <div class="indent">
                        % if assigned_user['user_id'] == user.id:
                            <a href="/user?user_id=${assigned_user['user_id']}">${assigned_user['user']}</a>
                            <small>( owner )</small>
                        % else:
                            <a href="/user?user_id=${assigned_user['user_id']}">${assigned_user['user']}</a> 
                            <small>( <a href="#">remove</a> )</small>
                        % endif
                        </div>
                    % endfor
                    </div>
                </div>
                
                
            </div>
            <hr/>
        </div>
    </div>
    
    <script>
    
        function add_user(email, name) {
            
            //var email = $('#email').val();
            
            if ( email != '' ) {
            
                url = '/assign_user_to_project.json'
                $.ajax({
                    dataType: 'json',
                    type: 'POST',
                    data: {
                        project_id : ${project['id']},
                        email : email,
                    },
                    url: url,
                    success: function(data) {
                        if( data.success == true ) {
                            //if ( data.assignment_id = -1 ) {
                            //    alert('User already assigned to project');
                            //}
                            window.location.href="/projectsettings?project_id=${project['id']}";
                        } else {
                            $('#error-field').html(name + ' already assigned to project');
                            $('#error-field').addClass('error-field');
                        }
                    },
                    error: function(data) {
                        alert('Invalid email address, please try again.');
                    }
                });
            }
        }
    
        $(document).ready( function() {
        
            $('#assigned-drop').on('click', function(e) {
                assigned_user_email = $(e.target).attr('user_email');
                assigned_user_name = $(e.target).attr('user_name');
                //$('#assigned-name').html(assigned_user_name);
                
                $('#assigned-drop').removeClass('open');
                $('#assigned-drop').css('left', '-99999px');
                
                add_user(assigned_user_email, assigned_user_name);
            });
        
        });
    
    </script>
