<%inherit file="base.mak"/>

    % if not user:
    
    <script>
        window.location.href = "/login";
    </script>
    
    % else:

    <style>

    </style>

    <div class="row">
        <div class="medium-12 columns bottom-border">
            <a href="/">Home</a>
             > 
            <a href="/users">Users</a>
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
        <!--
        <div class="medium-4 columns">
            <h5>Collections</h5>
            <div class="box shadow list-container">
                <div class="box-title">
                    Projects
                    <div class="right">
                        <a href="/newproject">New Project</a>
                    </div>
                </div>
                % if not projects:
                    <div class="indent">
                        <div class="small-light-text">No projects yet.</div>
                    </div>
                % else:
                    % for project in projects:
                        <!--<div class="indent">-->
                        <div class="box-inner-container">
                            <a href="/project?project_id=${project['id']}">${project['name']}</a>
                            <div class="right">
                                
                            </div>
                        </div>
                    % endfor
                    % if len(projects) > 5:
                        <div class="row">
                            <div class="medium-12 columns">
                                <div class="right" style="padding-right: 5px;">
                                    <a href="/projects">view all</a>
                                </div>
                            </div>
                        </div>
                    % endif
                % endif
            </div>
            <hr/>
        </div>
        -->
        
        <div class="medium-8 columns">
            <h5>Activity<h5>
            <div class="row">
                <div class="small-12 columns">
                    % if actions:
                        % for action in actions:
                        <div class="action-box shadow">
                            <div class="small-light-text">${str(action['created']).split('.')[0]}</div>
                            <a href="/user?user_id=1">Tim Duffy</a>
                            ${action['action'][0].upper()}${action['action'][1:]} 
                            % if action['subject'] == 'project':
                                a new project <a href="/project?project_id=${action['project_id']}">${action['project_name']}</a>.
                            % elif action['subject'] == 'ticket':
                                a new ticket <a href="/ticket?ticket_id=${action['ticket_id']}">${action['ticket_title']}</a> in
                                <a href="/project?project_id=${action['project_id']}">${action['project_name']}</a>.
                            % elif action['subject'] == 'ticket_comment':
                                a comment to a ticket <a href="/ticket?ticket_id=${action['ticket_id']}">${action['ticket_title']}</a>.
                            % elif action['subject'] == 'task':
                                a new task <a href="/task?task_id=${action['task_id']}">${action['task_title']}</a> in
                                <a href="/project?project_id=${action['project_id']}">${action['project_name']}</a> 
                            % endif
                        </div>
                        % endfor
                    % else:
                        <div class="small-light-text">
                            ${target_user.first} ${target_user.last} hasn't generated any activity yet.
                        </div>
                    % endif
                    
                </div>
            </div>
            <hr/>
        </div>
    
    % endif