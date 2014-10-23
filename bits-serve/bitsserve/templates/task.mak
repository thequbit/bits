<%inherit file="base.mak"/>

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
        
 
    </style>

    <div class="row">
        <div class="large-12 columns bottom-border">
            <a href="/">Home</a>
             > 
            <a href="/project?project_id=${project['id']}">Project</a>
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
                <h3><div class="task-title">Task</div> : ${task['title']}</h3>
                <div class="small-light-text">
                    Opened by ${task['owner']} on ${task['created']}
                </div>
                <div class="indent indent-right">
                    <div class="box shadow">
                        <div class="container-inner">
                            ${task['contents'] | n}
                        </div>
                    </div>
                </div>
                <br/>           
 
                <h5>Comments</h5>            
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
        % endif
        </div>
        <div class="medium-4 columns">
            <div class="box shadow">
                <div class="box-title">
                    Existing Tasks
                    <!--<div class="right">
                        <a href="/newtask?project_id=${project['id']}">New</a>
                    </div>-->
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

        $('#submit-comment').on('click', function(e) {
            
            console.log('sending comment')
            
            var token = document.cookie.split('=')[1]; 
            var url = '/create_comment.json?token=' + token;
            var task_id = ${task['id']}
            //var author_id = localStorage.getItem("user_id")
            //var project_id = ${project['id']};
            var contents = $('#comment-contents').val();
            
            $.ajax({
                dataType: 'json',
                type: 'POST',
                data: {
                    task_id : task_id,
                    //author_id : author_id,
                    //project_id : project_id,
                    contents : contents
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

        // TODO: hook up submit and close button

    </script>