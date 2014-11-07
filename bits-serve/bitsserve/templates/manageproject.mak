<%inherit file="managementbase.mak"/>

    <script src="static/js/dhtmlxgantt/dhtmlxgantt.js" type="text/javascript" charset="utf-8"></script>
    <link rel="stylesheet" href="static/css/dhtmlxgantt/dhtmlxgantt.css" type="text/css" media="screen" title="no title" charset="utf-8">

    

    <style>
    
        div.left-nav {
            float: left;
            width: 15%;
            min-width: 250px;
            background-color: rgba(0, 140, 186, 0.2) !important;
            margin-right: 10px;
            /*height: 100%;*/
            margin-left: 10px;
            padding-bottom: 25px;
        }
        
        div.project-name {
            font-size: 110%;
            /*border-bottom: 1px solid #333;*/
            margin-top: 10px;
            margin-left: 25px;
            margin-right: 25px;
            /*font-weight: bold;*/
        }

        div.left-nav-links {
            margin-left: 35px;
            margin-top: 10px;
            margin-bottom: 10px;
            border-bottom: 1px solid #333;
            margin-right: 55px;
            padding-bottom: 10px;
        }
        
        div.left-nav-links a {
            
        }
        
        div.content-area {
            float: left;
            width: 83%;
            min-width: 1000px;
            margin-right: 10px;
            height: 100%
            min-height: 800px;
        }
        
        div.content-page {
            padding: 10px 10px 10px 10px;
            border: 1px solid #EEE;
        }
        
        div.management-bread-crumbs {
            margin-bottom: 8px;
            margin-left: 25px;
        }
        
        div.tasks-container {
            width: 60%;
            padding: 10px 10px 10px 10px;
            border: 1px solid #DDD;
        }
        
        div.task-info-container {
            flex-grow: 1;
            margin-left: 25px;
            padding: 10px 10px 10px 10px;
            border: 1px solid #DDD;
        }
        
        
    </style>
    
    <div class="management-bread-crumbs">
        <a href="/">Home</a>
         > 
        <a href="/projects">Projects</a>
         >
        <a href="/project?project_id=${project['id']}">Test Project</a>
         > 
        Manage
    </div>
    
    <div class="left-nav">
        <div class="project-name">
            <h4>${project['name']} <small>${project['owner']}</small></h4>
        </div>
        
        <div class="left-nav-links">
        </div>
        <div class="left-nav-links">
            <a href="#" id="link-gantt">Gantt</a>
            <br/>
            <a href="#" id="link-resources">Resources</a>
            <br/>
            <a href="#" id="link-assignees">Assignees</a>
            <br/>
        </div>
        <div class="left-nav-links">
            <a href="#" id="link-tasks">Tasks</a>
            <br/>
            <a href="#" id="link-tickets">Tickets</a>
            <br/>
            <a href="#" id="link-lists">Lists</a>
            <br/>
            <a href="#" id="link-requirements">Requirements</a>
            <br/>
            <a href="#" id="link-milestones">Milestones</a>
            <br/>
            <a href="#" id="link-notes">Notes</a>
            <br/>
        </div>
        <div class="left-nav-links">
            <a href="#" id="link-reports">Reports</a>
            <br/>
        </div>
        
    </div>
    
    <div class="content-area" id="content-area">
    
        <div class="content-page" id="page-gantt">
            <h5>Project Gantt Chart</h5>
            <div>
                <div class="indent" id="scale-container">
                    <input type="radio" id="scale1" name="scale" value="1" checked /><label for="scale1">Day</label>
                    <input type="radio" id="scale2" name="scale" value="2" /><label for="scale2">Week</label>
                    <input type="radio" id="scale3" name="scale" value="3" /><label for="scale3">Month</label>
                    <input type="radio" id="scale4" name="scale" value="4" /><label for="scale4">Year</label>
                </div>
            </div>
            
            <div style="width: 100%; height: 900px;">
                <div id="gantt-chart-container" style='width:100%; height:100%;'></div>
            </div>
        </div>
        
        <div class="content-page" id="page-resources" style="display: none;">
            <h5>Project Resources</h5>
        </div>
        
        <div class="content-page" id="page-assignees" style="display: none;">
            <h5>Project Assignees</h5>
        </div>
        
        
        <div class="content-page" id="page-tasks" style="display: none;">
            <h5>Project Tasks</h5>
            
            <div style="display: flex;">
                <div class="tasks-container">
                    <div class="right"><a href="newtask?project_id=${project['id']}">New Task</a></div>
                    <h6>Task List</h6>
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
                <div class="task-info-container">
                    <h6>Task Info</h6>
                </div>
            </div>
            
        </div>
        
        <div class="content-page" id="page-tickets" style="display: none;">
            <h5>Project Tickets</h5>
        </div>
        
        <div class="content-page" id="page-lists" style="display: none;">
            <h5>Project Lists</h5>
        </div>
        
        <div class="content-page" id="page-requirements" style="display: none;">
            <h5>Project Requirements</h5>
        </div>
        
        <div class="content-page" id="page-milestones" style="display: none;">
            <h5>Project Milestones</h5>
        </div>
        
        <div class="content-page" id="page-notes" style="display: none;">
            <h5>Project Notes</h5>
        </div>
        
        
        <div class="content-page" id="page-reports" style="display: none;">
            <h5>Project Reports</h5>
        </div>
    </div>
    
    
    <script type="text/javascript">
        
        var pages = [
            "gantt",
            "resources",
            "assignees",
            
            "tasks",
            "tickets",
            "lists",
            "requirements",
            "milestones",
            "notes",
            
            "reports",
        ];
        
        function hide_pages() {
            pages.forEach( function(page_name) {
                $('#page-' + page_name).hide();
            });
        }
       
        $('.left-nav a').on('click', function(e) {
            
            target_page_name = e.target.id.split('-')[1];
            
            console.log(target_page_name);
            
            hide_pages();
            
            $('#page-' + target_page_name).show();
        });
        
        
        
        function set_gantt_scale(value) {
        
            console.log('switching to scale value ' + value);
        
            switch (value) {
            
                case "1":
                    gantt.config.scale_unit = "day";
                    gantt.config.step = 1;
                    gantt.config.date_scale = "%d %M";
                    gantt.config.subscales = [];
                    gantt.config.scale_height = 25;
                    gantt.templates.date_scale = null;

                    break;
                    
                case "2":
                    var weekScaleTemplate = function(date){
                        var dateToStr = gantt.date.date_to_str("%d %M");
                        var endDate = gantt.date.add(gantt.date.add(date, 1, "week"), -1, "day");
                        return dateToStr(date) + " - " + dateToStr(endDate);
                    };

                    gantt.config.scale_unit = "week";
                    gantt.config.step = 1;
                    gantt.templates.date_scale = weekScaleTemplate;
                    gantt.config.subscales = [
                        {unit:"day", step:1, date:"%D" }
                    ];
                    gantt.config.scale_height = 50;
                    
                    break;
                    
                case "3":
                    gantt.config.scale_unit = "month";
                    gantt.config.date_scale = "%F, %Y";
                    gantt.config.subscales = [
                        {unit:"day", step:1, date:"%j, %D" }
                    ];
                    gantt.config.scale_height = 50;
                    gantt.templates.date_scale = null;
                    
                    break;
                    
                case "4":
                    gantt.config.scale_unit = "year";
                    gantt.config.step = 1;
                    gantt.config.date_scale = "%Y";
                    gantt.config.min_column_width = 50;

                    gantt.config.scale_height = 50;
                    gantt.templates.date_scale = null;

                    
                    gantt.config.subscales = [
                        {unit:"month", step:1, date:"%M" }
                    ];
                    
                    break;
                    
            }
            
        }

        $(document).ready( function() {

            $('#scale-container').on('click', function(e) {
                set_gantt_scale(e.target.value);
                gantt.render();
            });

            // projects - 1000
            // tasks    - 2000
            //

            var tasks =  {
            data:[
                {
                    id: 1000${project['id']},
                    text: "${project['name']}",
                    start_date: "${project['creation_date_formatted']}",
                    //duration:365,
                    //order:10,
                    //progress:0.4,
                    open: true
                },
                % for task in tasks:
                    {
                        id: 2000${task['id']},
                        text:"${task['title']}",
                        start_date:"${task['creation_date_formatted']}",
                        duration:${task['duration']},
                        //order:10,
                        //progress:0.6,
                        parent:1000${project['id']}
                    },
                % endfor
                /*
                {
                    id:2,
                    text:"Task #1",
                    start_date:"02-04-2013",
                    duration:8,
                    order:10,
                    progress:0.6,
                    parent:1
                },
                {
                    id:3,
                    text:"Task #2",
                    start_date:"11-04-2013",
                    duration:8,
                    order:20,
                    progress:0.6,
                    parent:1
                }
                */
            ],
            links:[
                /*
                { id:1, source:1, target:2, type:"1"},
                { id:2, source:2, target:3, type:"0"},
                { id:3, source:3, target:4, type:"0"},
                { id:4, source:2, target:5, type:"2"},
                */
            ]
        };

            /*
            gantt.config.subscales = [
                {unit:"month", step:1, date:"%M" },
                {unit:"year", step:1, date:"%Y" }
            ];
            
            gantt.config.scale_height = 2*28;
            */
            
            gantt.init(
                "gantt-chart-container",
                "${project['creation_date_formatted']}"
            );

            gantt.parse(tasks);
            
            // start with the year view
            $('#scale4').prop('checked',true);
            set_gantt_scale('4');
            gantt.render();
        
        });

    </script>