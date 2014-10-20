<%inherit file="base.mak"/>

    <style>
    
        div.actions-feed {
        }

        div.action-box {
            padding: 10px;
            /*border-top: 1px solid #DDD;*/
        }

        div.action-box {
        /*    box-shadow: 0px 0px 0px 1px #DDD, 0px 4px 8px rgba(221, 221, 221, 0.9);*/
            margin-top: 10px;
            /*margin-bottom: 20px;*/
        }

        div.action-box p {
            color: #BBB;
            margin-top: 10px;
            font-size: 70%;
            padding-left: 20px;
        }

        div.small-light-text {
            font-size: 80%;
            color: #BBB;
        }

        /*
        div.box {
            padding: 5px;
            border: 2px solid #DDD;
            border-radius: 4px;
        }
        
        div.box-title {
            margin-bottom: 6px;
            border-bottom: 2px solid #DDD;
            border-top-left-radius: 4px;
            border-rop-right-radius: 4px;
            padding-bottom: 2px;
        }

        div.box-small-text {
            font-size: 80%;
        }
        
        div.box-small-text b {
            padding-right: 5px;
        }

        div.indent {
            padding-left: 20px;
        }
        */

    </style>

    % if user and token:

    <div class="row">
        <div class="medium-12 columns bottom-border">
            <div class="right top-links">
                <a href="/usersettings?user_id=${user.id}">${user.first} ${user.last}</a>
            </div>
        </div>
    </div>
    <br/>
    <div class="row">
         <div class="medium-4 columns">
            <div class="row">
            <div class="medium-12 columns">
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
                            <!--
                            <div class="box-small-text">r:<b>${project['requirement_count']}</b>t:<b>${project['ticket_count']}</b>n:<b>${project['note_count']}</b></div>
                            -->
                        </div>
                    </div>
                    % endfor
                    % if len(projects) > 5:
                    <div class="row">
                        <div class="medium-12 columns">
                            <div class="right" style="padding-right: 5px;">
                                <a href="/tickets?project_id=${project['id']}">view all</a>
                            </div>
                        </div>
                    </div>
                    % endif
                % endif
            </div>
            <hr/>
            </div>
            </div>
        </div>

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
                    % endif
                </div>
            </div>
        </div>

    </div>

    % endif

