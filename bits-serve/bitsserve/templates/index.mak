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
        <div class="medium-6 columns">
            <!--<h5>Collections</h5>-->
            <div class="box shadow list-container">
                <div class="box-title">
                    <a href="/projects">Projects</a>
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
                        
                        <div class="box-inner-container">
                            <h5><a href="/project?project_id=${project['id']}">${project['name']}</a></h5>
                            
                            <div class="indent">
                            
                                % if len(project['ticket_assignments']) != 0:
                                
                                    <h7>
                                        <div class="plus-link">
                                            <a id="${ sanitize(project['name']) }-tickets-link">+</a>
                                        </div>
                                        Tickets <small>assigned to ${user.first} ${user.last}.</small>
                                    </h7>
                                
                                    % for ticket_assignment in project['ticket_assignments']:
                                        
                                        <div class="bottom-buffer">
                                        
                                            <div class="indent ${ sanitize(ticket_assignment['project_name']) }-ticket-item" style="display: none;">
                                                <div class="box shadow ticket-container">
                                                
                                                    <h5>
                                                        <div class="">
                                                            <!--<a href="/project?project_id=${ticket_assignment['project_id']}">${ticket_assignment['project_name']}</a> : -->
                                                            <a class="small-indent" href="/ticket?ticket_id=${ticket_assignment['id']}">${ticket_assignment['title']}</a>
                                                            <div class="small-text indent">
                                                                #${ticket_assignment['number']} opened by <a href="/user?user_id=${user.id}">${ticket_assignment['owner']}</a> on ${ticket_assignment['created']}
                                                            </div>
                                                        </div>
                                                    </h5>

                                                </div>
                                            </div>
                                        
                                        </div>
                                        
                                    % endfor
                                % else:
                                    <!--<div class="indent small-light-text">You have no tickets assigned to you.</div>-->
                                % endif
                                
                            </div>
                            
                            <div class="indent">
                            
                                % if len(project['task_assignments']) != 0:
                                
                                    <h7>
                                        <div class="plus-link">
                                            <a id="${ sanitize(project['name']) }-tasks-link">+</a>
                                        </div>
                                        Tasks <small>assigned to ${user.first} ${user.last}.</small>
                                    </h7>
                                
                                    % for task_assignment in project['task_assignments']:
                                        
                                        <div class="bottom-buffer">
                                            
                                            <div class="indent ${ sanitize(task_assignment['project_name']) }-task-item" style="display: none;">
                                                <div class="box shadow ticket-container">
                                                
                                                    <h5>
                                                        <div class="">
                                                            <!--<a href="/project?project_id=${task_assignment['project_id']}">${task_assignment['project_name']}</a> : -->
                                                            <a class="small-indent" href="/task?task_id=${task_assignment['id']}">${task_assignment['title']}</a>
                                                            <div class="small-text indent">
                                                                Opened by <a href="/user?user_id=${user.id}">${task_assignment['owner']}</a> on ${task_assignment['created']}
                                                            </div>
                                                        </div>
                                                    </h5>

                                                </div>
                                            </div>
                                        
                                        </div>
                                        
                                    % endfor
                                % else:
                                    <!--<div class="indent small-light-text">You have no tasks assigned to you.</div>-->
                                % endif
                            
                            </div>
                            
                            <!--
                            <div class="right">
                                
                            </div>
                            -->
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
        
    </div>
    
    <div class="row">
        <div class="medium-12 columns">
            <h4>Project Activity <small> that ${user.first} ${user.last} is assigned to.</small></h4>
            
            <!--<div class="top-bottom-border">-->
                
                <!--<div class="plus-link"><a id="hide-show-activity">+</a></div>-->
                <div id="activity-container" class="indent">
            
                    % if actions:
                        % for action in actions:
                        <div class="action-box shadow">
                            <div class="small-light-text">${str(action['created']) .split('.')[0]}</div>
                            ${action['contents'] | n}
                        </div>
                        % endfor
                    % else:
                        <div class="small-light-text">There are no activity for hte projects you are assigned to.</div>
                    % endif
                    
                </div>
            <!--</div>-->
 
        </div>
    </div>
    
    <script>
    
        <%! from bitsserve.utils import sanitize %>
    
        $(document).ready( function() {
            % for project in projects:
                // tickets for ${ project['name'] }
                % for ticket_assignment in project['ticket_assignments']:
                    % if ticket_assignment != None:
                        % if ticket_assignment['header'] == True:
                            $('#${ sanitize(ticket_assignment['project_name']) }-tickets-link').on('click', function(e) {
                                if ( $('div.${ sanitize(ticket_assignment['project_name']) }-ticket-item').is(":visible") ) {
                                    console.log('hiding ticket_assignment');
                                    $('div.${ sanitize(ticket_assignment['project_name']) }-ticket-item').hide();
                                    $('#${ sanitize(ticket_assignment['project_name']) }-tickets-link').html('+');
                                } else {
                                    console.log('showing ticket_assignment');
                                    $('div.${ sanitize(ticket_assignment['project_name']) }-ticket-item').show();
                                    $('#${ sanitize(ticket_assignment['project_name']) }-tickets-link').html('-');
                                }
                                
                            });
                        % endif
                    % endif
                % endfor
                
                // tasks for ${ project['name'] }
                % for task_assignment in project['task_assignments']:
                    % if task_assignment != None:
                        % if task_assignment['header'] == True:
                            $('#${ sanitize(task_assignment['project_name']) }-tasks-link').on('click', function(e) {
                                if ( $('div.${ sanitize(task_assignment['project_name']) }-task-item').is(":visible") ) {
                                    console.log('hiding task_assignment');
                                    $('div.${ sanitize(task_assignment['project_name']) }-task-item').hide();
                                    $('#${ sanitize(task_assignment['project_name']) }-tasks-link').html('+');
                                } else {
                                    console.log('showing task_assignment');
                                    $('div.${ sanitize(task_assignment['project_name']) }-task-item').show();
                                    $('#${ sanitize(task_assignment['project_name']) }-tasks-link').html('-');
                                }                            
                            });
                        % endif
                    % endif
                % endfor

            % endfor
        });
        
    
        
    
    </script>
