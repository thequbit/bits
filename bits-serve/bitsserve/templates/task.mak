<%inherit file="base.mak"/>

    % if not task:
    
    <script>
        window.location.href = "/login";
    </script>
    
    % else:

    <style>
    
        div.task-container {
            border-bottom: 1px solid #DDD;
            padding-bottom: 5px;
        }

        div.task {
            margin-top: 10px;
            border: 1px solid #DDD;
            padding: 15px;15px
        }

        textarea {
           min-height: 150px;
        }

        div.task-container h3 {
            margin-bottom: 0rem !important;
        }

        div.comment-container {
            
        }

        div.container-inner {
            padding: 10px;            
        }
        
        div.container-inner p {
            margin-bottom: 0px !important;
        }
        
        h4.complete-label {
            margin-left: 20px;
            color: #008000;
            font-weight: bold;
        }
        
        div.due-lable {
            padding-top: 10px;
        }
        
 
    </style>

    <div class="row">
        <div class="large-12 columns bottom-border">
            <a href="/">Home</a>
             > 
            <a href="/project?project_id=${project['id']}">Project</a>
             > 
            <a href="/tasks?project_id=${project['id']}">Tasks</a>
             > Task
            <div class="right top-links">
                <a href="/usersettings">${user.first} ${user.last}</a>
            </div>
        </div>
    </div>


    <div class="row">
        <div class="medium-8 columns">
        % if task:
            <div class="task-container">
                <div id="task-title" style="display: inline-flex;">
                    <h4>Ticket : ${task['title']}
                    <!--
                    % if task['completed'] == False:
                        <small>
                            <a href="#" id="edit-task-title">edit</a>
                        </small>
                    % endif
                    -->
                    </h4>
                    % if task['completed'] == True:
                        <h4 class="complete-label">[COMPLETE]</h4>
                    % endif
                </div>
                <div class="small-light-text">
                    Opened by ${task['owner']} on ${task['created']}
                </div>
                <div class="small-text due-lable" >
                    Due on ${task['due'].split(' ')[0]}.
                </div>
                <div class="indent indent-right">
                    <div class="box shadow">
                        <div class="container-inner">
                            ${task['contents'] | n}
                        </div>
                    </div>
                </div>
                <br/>
                <div class="right indent-right">
                    <a href="#" id="mark-complete" class="small radius button">Mark Complete</a>
                </div>
                <br/><br/><br/>
                
               
            </div>
        % endif
        </div>
        
        <div class="medium-4 columns">
            <div class="box shadow">
                <div class="box-title">
                    Existing Tasks
                    <div class="right">
                        <a href="/newtask?project_id=${project['id']}">New Task</a>
                    </div>
                </div>
                % if not tasks:
                    <div class="indent">
                        <div class="small-light-text">No tasks for this project.</div>
                    </div>
                % else:
                    % for existing_task in tasks:
                        <div class="box-inner-container">
                            <a href="/task?task_id=${existing_task['id']}">${existing_task['title']}</a>
                            <div class="short-line-height extra-small-light-text"> opened by ${existing_task['owner']} on ${existing_task['created']}</div>
                        </div>
                    % endfor
                % endif
            </div>
        </div> 
    </div>

    <script>

        $('#mark-complete').on('click', function(e) {
            
            var token = document.cookie.split('=')[1]; 
            var url = '/complete_task.json?token=' + token;
            var task_id = ${task['id']}
            
            $.ajax({
                dataType: 'json',
                type: 'POST',
                data: {
                    task_id : task_id,
                },
                url: url,
                success: function(data) {
                    if( data.success == true ) {
                        console.log('SUCCESS!');
                        window.location.href="/task?task_id=${task['id']}";
                    }
                },
                error: function(data) {
                    console.log('an error happened while creating task ...');
                    // TODO: report error
                }
            });
           
        });

    </script>
    
    % endif