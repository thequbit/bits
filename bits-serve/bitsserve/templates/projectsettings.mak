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
                    Manage the users that have access to this project.<br/><br/>
                </div>
                <div class="assigned-contianer">
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
                <div class="container-inner">
                    <div><input id="email" type="text" placeholder="participant email"></input></div>
                    <div class="right">
                        <a href="#" id="add-user">Add User</a>
                    </div>
                    </br>
                </div>
                
            </div>
            <hr/>
        </div>
    </div>
    
    <script>
    
        function add_user() {
            
            var email = $('#email').val();
            
            if ( email != '' ) {
            
                url = '/assign_user.json'
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
                            if ( data.assignment_id = -1 ) {
                                alert('User already assigned to project');
                            }
                            window.location.href="/projectsettings?project_id=${project['id']}";
                        }
                    },
                    error: function(data) {
                        alert('Invalid email address, please try again.');
                    }
                });
            }
        }
    
        $(document).ready( function() {
        
            $('#add-user').on('click', function(e) {
                add_user();
            })
        
        });
    
    </script>
