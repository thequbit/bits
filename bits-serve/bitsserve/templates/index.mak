<%inherit file="base.mak"/>

    <style>

    </style>

    <div class="row">
        <div class="large-12 columns bottom-border">
            Home
            <div class="right top-links">
                <a href="/usersettings">${user.first} ${user.last}</a>
            </div>
        </div>
    </div>

    <br/>
    
    <div class="row">
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
            
            <!--
            <div class="box shadow list-container">
                <div class="box-title">
                    Customers
                    <div class="right">
                        <a href="/newcustomer">New Customer</a>
                    </div>
                </div>
                % if not customers:
                    <div class="indent">
                        <div class="small-light-text">No customers yet.</div>
                    </div>
                % else:
                    % for customer in customers:
                        <!--<div class="indent">-->
                        <div class="box-inner-container">
                            <a href="/customer?customer_id=${customer['id']}">${customer['name']}</a>
                            <div class="right">
                                
                            </div>
                        </div>
                    % endfor
                    % if len(customers) > 5:
                        <div class="row">
                            <div class="medium-12 columns">
                                <div class="right" style="padding-right: 5px;">
                                    <a href="/customers">view all</a>
                                </div>
                            </div>
                        </div>
                    % endif
                % endif
            </div>
            -->
            
        </div>

        <div class="medium-8 columns">
            <div class="row">
                <div class="small-12 columns">
                    <h4>Ticket Assignments <small>Ticket assigned to ${user.first} ${user.last}</small></h4>
                    % if ticket_assignments:
                        % for ticket_assignment in ticket_assignments:
                        <div class="box shadow ticket-container">
                            <h5>
                                <div class="">
                                    <a href="/project?project_id=${ticket_assignment['project_id']}">${ticket_assignment['project_name']}</a> : 
                                    <a href="/ticket?ticket_id=${ticket_assignment['id']}">${ticket_assignment['title']}</a>
                                    <div class="small-text indent">
                                        #${ticket_assignment['number']} opened by <a href="/user?user_id=${user.id}">${ticket_assignment['owner']}</a> on ${ticket_assignment['created']}
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
                    % else:
                        <div class="small-light-text">You have no tickets assigned to you.</div>
                    % endif
                </div>
            </div>
            <hr/>
        </div>
        
        <div class="medium-8 columns">
            <div class="row">
                <div class="small-12 columns">
                    <h4>Task Assignments <small>Tasks assigned to ${user.first} ${user.last}</small></h4>
                    % if task_assignments:
                        % for task_assignment in task_assignments:
                        <div class="box shadow ticket-container">
                            <h5>
                                <div class="">
                                    <a href="/project?project_id=${task_assignment['project_id']}">${task_assignment['project_name']}</a> : 
                                    <a href="/ticket?ticket_id=${task_assignment['id']}">${task_assignment['title']}</a>
                                    <div class="small-text indent">
                                        Opened by <a href="/user?user_id=${user.id}">${task_assignment['owner']}</a> on ${task_assignment['created']}
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
                    % else:
                        <div class="small-light-text">You have no tasks assigned to you.</div>
                    % endif
                </div>
            </div>
            <hr/>
        </div>
        
        <div class="medium-8 columns">
            <div class="row">
                <div class="small-12 columns">
                    <h4>Project Activity <small>Project activity for projects ${user.first} ${user.last} is assigned to</small></h4>
                    % if actions:
                        % for action in actions:
                        <div class="action-box shadow">
                            <div class="small-light-text">${str(action['created']).split('.')[0]}</div>
                            ${action['contents'] | n}
                        </div>
                        % endfor
                    % endif
                </div>
            </div>
            <hr/>
        </div>

    </div>
