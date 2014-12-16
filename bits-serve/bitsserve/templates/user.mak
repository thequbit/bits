<%inherit file="base.mak"/>

    <style>

        div.action-item {
            /* dummy for jquery call */
        }


    </style>

    <div class="row">
        <div class="medium-12 columns bottom-border">
            <a href="/">Home</a>
             > 
            <!--<a href="/users">Users</a>--> Users 
             >
            ${user.first} ${user.last}
            <div class="right top-links">
                <a href="/usersettings">${user.first} ${user.last}</a>
            </div>
        </div>
    </div>
    <br/>

    <div class="row">
        <div class="medium-12 columns">
            <h5>${target_user.first} ${target_user.last}</h5>
            <!--
            <div class="box shadow">
                <div class="container-inner">
                    <p></p>
                </div>
            </div>
            -->
        </div>
    </div>
   
    <div class="row">
        <div class="medium-12 column">
            <div style="display: inline-block; margin-left: 20px;">
                <a href="/user?user_id=${target_user.id}&assignments=0">User Activity</a>
                % if assignments == False:
                    <div style="background-color: #008CBA !important; height: 3px;"></div>
                % endif
            </div>
            <div style="display: inline-block; margin-left: 20px;">
                <a href="/user?user_id=${target_user.id}&assignments=1">User Assignments</a>
                % if assignments == True:
                    <div style="background-color: #008CBA !important; height: 3px;"></div>
                % endif
            </div>
            <!--
            <div class="right">
                <a href="/">New Task</a>
            </div>
            -->
        </div>
    </div>

    % if assignments == False: 
    <div class="row">
        <div class="medium-8 columns">
            <div class="row">
                <div id="project-actions" class="small-12 columns">
                    % for action in actions:
                        % if action != None:
                        % if action['header'] == True:
                            <br/>
                            <hr/>
                            <h5>${action['project_name']}</h5>
                            <div class="indent">
                            <a id="${action['project_name'].replace(' ','-')}-link">Show Actions</a>
                            </div>
                        % endif
                        <div class="indent ${action['project_name'].replace(' ','-')}-item" style="display: none;">
                            <div class="action-box shadow">
                                <div class="small-light-text">${str(action['created']).split('.')[0]}</div>
                                ${action['contents'] | n}
                            </div>
                        </div>
                        % endif
                    % endfor
                    
                </div>
            </div>
            <hr/>
        </div>
    </div>

    <script>
        
        $(document).ready( function() {

            % for action in actions:
                % if action != None:
                    % if action['header'] == True:
                        $('#${action['project_name'].replace(' ','-')}-link').on('click', function(e) {
                            console.log('click!');
                            if ( $('div.${action['project_name'].replace(' ','-')}-item').is(":visible") ) {
                                console.log('hiding actions');
                                $('div.${action['project_name'].replace(' ','-')}-item').hide();
                                $('#${action['project_name'].replace(' ','-')}-link').html('Show Actions');
                            } else {
                                console.log('showing actions');
                                $('div.${action['project_name'].replace(' ','-')}-item').show();
                                $('#${action['project_name'].replace(' ','-')}-link').html('Hide Actions');
                            }
                            
                            return false;
                            
                        });
                    % endif
                % endif
            % endfor

            // show the first project list of actions on the page
            $('div.${actions[0]['project_name'].replace(' ','-')}-item').show();
            $('#${actions[0]['project_name'].replace(' ','-')}-link').html('Hide Actions');

        });

    </script>
    
    % else:
    
    <br/><br/>
    <div class="row">
        <div class="medium-8 columns">
            <h5>Ticket Assignments</h5>
            % if ticket_assignments:
                % for ticket_assignment in ticket_assignments:
                <div class="box shadow ticket-container">
                    <h5>
                        <div class="">
                            <a href="/project?project_id=${ticket_assignment['project_id']}">${ticket_assignment['project_name']}</a> : 
                            <a href="/ticket?ticket_id=${ticket_assignment['id']}">${ticket_assignment['title']}</a>
                            <div class="small-text indent">
                                #${ticket_assignment['number']} opened by <a href="/user?user_id=${target_user.id}">${ticket_assignment['owner']}</a> on ${ticket_assignment['created']}
                            </div>
                        </div>
                    </h5>
                    <!--
                    <div class="container-inner">
                        ${ticket_assignment['contents'] | n}
                    </div>
                    -->
                </div>
                % endfor
            % endif
     
            <hr/>

            <h5>Task Assignments</h5>
            % if task_assignments:
                % for task_assignment in task_assignments:
                <div class="box shadow task-container">
                    <h5>
                        <div class="">
                            <a href="/project?project_id=${task_assignment['project_id']}">${task_assignment['project_name']}</a> : 
                            <a href="/ticket?ticket_id=${task_assignment['id']}">${task_assignment['title']}</a>
                            <div class="small-text indent">
                                Opened by <a href="/user?user_id=${target_user.id}">${task_assignment['owner']}</a> on ${task_assignment['created']}
                            </div>
                        </div>
                    </h5>
                    <!--
                    <div class="container-inner">
                        ${task_assignment['contents'] | n}
                    </div>
                    -->
                </div>
                % endfor
            % endif
            <hr/>
        </div>
    </div>
    
    
    % endif
