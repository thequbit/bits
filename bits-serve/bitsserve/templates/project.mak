<%inherit file="base.mak"/>

    % if not project:
    
    <script>
        window.location.href = "/login";
    </script>
    
    % else:

    <style>

        div.inner-container {
            margin-bottom: 10px;
        }

        div.inner-container .extra-small-light-text {
            line-height: 75% !important;
        }

        div.project-description {
            padding: 10px;
        }
        
        div.disabled {
            opacity: .25;
        }

    </style>
    
    <div class="row">
        <div class="medium-12 columns bottom-border">
            <a href="/">Home</a>
             > 
            Project
            <div class="right top-links">
                <a href="/projectsettings?project_id=${project['id']}">Settings</a>
                <a href="/usersettings">${user.first} ${user.last}</a>
            </div>
        </div>
    </div>
    <br/>

    <div class="row">
        <div class="medium-12 columns">
            <h5>${project['name']} <small>${project['owner']}</small></h5>
            <div class="box shadow">
                <div class="container-inner">
                    <p>${project['description']}</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="medium-4 columns">
            <div class="box shadow list-container">
                <div class="box-title">
                    <div class="task-title"><a href="/tasks?project_id=${project['id']}">Tasks</a></div>
                    <div class="right">
                        <a href="/newtask?project_id=${project['id']}">New</a>
                    </div>
                </div>
                % if not tasks:
                    <div class="indent">
                        <div class="small-light-text">No tasks for this project.</div>
                    </div>
                % else:
                    % for task in tasks[:5]:
                        <div class="box-inner-container">
                            <a href="/task?task_id=${task['id']}">${task['title']}</a>
                            <div class="short-line-height extra-small-light-text"> opened by ${task['owner']} on ${task['created']}</div>
                        </div>
                    % endfor
                    <div class="row">
                        <div class="medium-12 columns">
                            <div class="right" style="padding-right: 5px;">
                                <a href="/tasks?project_id=${project['id']}">view all</a>
                            </div>
                        </div>
                    </div>
                % endif                
            </div>
        </div>
        <div class="medium-4 columns">
            <div class="box shadow list-container">
                <div class="box-title">
                    <div class="ticket-title"><a href="/tickets?project_id=${project['id']}">Tickets</a></div>
                    <div class="right">
                        <a href="/newticket?project_id=${project['id']}">New</a>
                    </div>
                </div>
                % if not tickets:
                    <div class="indent">
                        <div class="small-light-text">No tickets for this project.</div>
                    </div>
                % else:
                    % for ticket in tickets[:5]:
                        <div class="box-inner-container">
                            <a href="/ticket?ticket_id=${ticket['id']}">${ticket['title']}</a>
                            <div class="short-line-height extra-small-light-text"> opened by ${ticket['owner']} on ${ticket['created']}</div>
                        </div>
                    % endfor
                    % if len(tickets) > 5:
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
        </div>
        <div class="medium-4 columns">
            <div class="box shadow list-container">
                <div class="box-title">
                    <div class="list-title"><a href="/lists?project_id=${project['id']}">Lists</a></div>
                    <div class="right">
                        <a href="/newlist?project_id=${project['id']}">New</a>
                    </div>
                </div>
                % if not lists:
                    <div class="indent">
                        <div class="small-light-text">No lists for this project.</div>
                    </div>
                % else:
                    % for list in lists[:5]:
                        <div class="box-inner-container">
                            <a href="/list?list_id=${list['id']}">${list['title']}</a>
                            <div class="short-line-height extra-small-light-text"> opened by ${list['owner']} on ${list['created']}</div>
                        </div>
                    % endfor
                    % if len(lists) > 5:
                    <div class="row">
                        <div class="medium-12 columns">
                            <div class="right" style="padding-right: 5px;">
                                <a href="/lists?project_id=${project['id']}">view all</a>
                            </div>
                        </div>
                    </div>
                    % endif
                % endif
            </div>
        </div>
    </div>
    <div class="row">
        <div class="medium-4 columns">
            <div class="box shadow list-container disabled">
                <div class="box-title"> 
                    <div class="requirement-title"><a href="/requirements?project_id=${project['id']}">Requirements</a></div>
                    <div class="right">
                        <!-- <a href="/newrequirment?project_id=${project['id']}">New</a> -->
                        <div style="color: #008CBA">New</div>
                    </div>
                </div>
                % if not requirements:
                    <div class="indent">
                        <div class="small-light-text">No requirements for this project.</div>
                    </div>
                % else:
                    % for requirement in requirements[:5]:
                        <div class="box-inner-container">
                            <a href="/requirement?requirement_id=${requirement['id']}">${requirement['name']}</a>
                            <div class="short-line-height extra-small-light-text"> opened by ${requirement['owner']} on ${requirement['created']}</div>
                        </div>
                    % endfor
                    % if len(requirements) > 5:
                    <div class="row">
                        <div class="medium-12 columns">
                            <div class="right" style="padding-right: 5px;">
                                <a href="/requirements?project_id=${project['id']}">view all</a>
                            </div>
                        </div>
                    </div>
                    % endif
                % endif                
            </div>
        </div>
        
        <div class="medium-4 columns">
            <div class="box shadow list-container disabled">
                <div class="box-title">
                    <div class="milestone-title"><a href="/milestones?project_id=${project['id']}">Milestones</a></div>
                    <div class="right">
                        <!--<a href="/newmilestone?project_id=${project['id']}">New</a>-->
                        <div style="color: #008CBA">New</div>
                    </div>
                </div>
                % if not milestones:
                    <div class="indent">
                        <div class="small-light-text">No milestones for this project.</div>
                    </div>
                % else:
                    % for milestone in milestones[:5]:
                        <div class="box-inner-container">
                            <div class="indent">
                                <a href="/milestone?ticket_id=${milestone['id']}">${milestone['title']}</a>
                                <div class="short-line-height extra-small-light-text"> opened by ${milestone['owner']} on ${milestone['created']}</div>
                            </div>
                        </div>
                    % endfor
                    % if len(milestone) > 5:
                    <div class="row">
                        <div class="medium-12 columns">
                            <div class="right" style="padding-right: 5px;">
                                <a href="/milestones?project_id=${project['id']}">view all</a>
                            </div>
                        </div>
                    </div>
                    % endif
                % endif
            </div>
        </div>
        
        <div class="medium-4 columns">
            <div class="box shadow list-container disabled">
                <div class="box-title">
                    <div class="note-title"><a href="/notes?project_id=${project['id']}">Notes</a></div>
                    <div class="right">
                        <!--<a href="/newnote?project_id=${project['id']}">New</a>-->
                        <div style="color: #008CBA">New</div>
                    </div>
                </div>
                % if not notes:
                    <div class="indent">
                        <div class="small-light-text">No notes for this project.</div>
                    </div>
                % else:
                    % for note in notes[:5]:
                        <div class="box-inner-container">
                            <div class="indent">
                                <a href="/note?ticket_id=${note['id']}">${note['title']}</a>
                                <div class="short-line-height extra-small-light-text"> opened by ${note['owner']} on ${note['created']}</div>
                            </div>
                        </div>
                    % endfor
                    % if len(notes) > 5:
                    <div class="row">
                        <div class="medium-12 columns">
                            <div class="right" style="padding-right: 5px;">
                                <a href="/notes?project_id=${project['id']}">view all</a>
                            </div>
                        </div>
                    </div>
                    % endif
                % endif
            </div>
        </div>
        
       
        
    </div>
    <hr/>
    
    % endif
