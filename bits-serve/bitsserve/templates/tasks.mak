<%inherit file="base.mak"/>

    <style>
    
        div.task-container a {
            /*padding-left: 2px;
            padding-top: 4px !important;*/
        }
    
    </style>
    
    <div class="row">
        <div class="medium-12 columns bottom-border">
            <a href="/">Home</a>
             >
            <a href="/project?project_id=${project['id']}">${project['name']}</a>
             > Tasks
            <div class="right top-links">
                <a href="/projectsettings?project_id=${project['id']}">Settings</a>
                <a href="/usersettings">${user.first} ${user.last}</a>
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="medium-12 column">
            <h5>Tasks</h5>
        </div>
    </div>
    
    <div class="row">
        <div class="medium-12 column">
            <div class="small-text bottom-border">
                % if completed == False:
                    Displayed below are all of the <b>open</b> tasks for the current project.
                % else:
                    Displayed below are all of the <b>completed</b> tasks for the current project.
                % endif
                <div class=" normal-text right">
                    <a href="/newtask?project_id=${project['id']}">New Task</a>
                </div>
            </div>
        </div>
    </div>
    
    <br/>

    <div style="display: inline-block; margin-left: 20px;">
        <a href="/tasks?project_id=${project['id']}&completed=0">Open Tasks</a>
        % if completed == False:
            <div style="background-color: #008CBA !important; height: 3px;"></div>
        % endif
    </div>
    <div style="display: inline-block; margin-left: 20px;">
        <a href="/tasks?project_id=${project['id']}&completed=1">Completed Tasks</a>
        % if completed == True:
            <div style="background-color: #008CBA !important; height: 3px;"></div>
        % endif
    </div>

    <div class="row">
        <div class="medium-12 columns">
        % if tasks and len(tasks) != 0:
            % for task in tasks:
                <div class="box shadow task-container">
                    <h5><div class="bottom-border"><a href="/task?task_id=${task['id']}">${task['title']}</a><h5>
                        <div class="small-text">Opened by <a href="/user?user_id=${user.id}">${task['owner']}</a> on ${task['created']}</div>
                        % if task['completed'] == True:
                            <div class="small-text">Completed <!-- by <a href="/user?user_id=${user.id}">${task['owner']}</a>-->on ${task['completed_datetime']}</div>
                        % endif
                    </div>
                    
                    <div class="container-inner">
                        ${task['contents'] | n}
                    </div>
                </div>
            % endfor
        % else:
            <div class="box small-light-text">
                % if completed == 0:
                    There are no open tasks for this project yet.
                % else:
                    There are no completed tasks for this project yet.
                % endif
            </div>
        % endif
        </div>
    </div>
    
    <hr/>
