<%inherit file="base.mak"/>

    <div class="row">
        <div class="large-12 columns bottom-border">
            <a href="/">Home</a>
             > 
            <a href="/project?project_id=${project['id']}">${project['name']}</a>
             > Tickets
            <div class="right top-links">
                <a href="/projectsettings?project_id=${project['id']}">Settings</a>
                <a href="/usersettings">${user.first} ${user.last}</a>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="medium-12 column">
            <div class="page-title">
                <div class="right manage-link">
                    <a href="/manageproject?project_id=${project['id']}">Manage Project</a>
                </div>
                <h4>Tickets</h4>
            </div>
        </div>
    </div>

    <br/><br/>
    
    
    <div class="row">
        <div class="medium-12 column">
            <div style="display: inline-block; margin-left: 20px;">
                <a href="/tickets?project_id=${project['id']}&closed=0">Open Tickets</a>
                % if closed == False:
                    <div style="background-color: #008CBA !important; height: 3px;"></div>
                % endif
            </div>
            <div style="display: inline-block; margin-left: 20px;">
                <a href="/tickets?project_id=${project['id']}&closed=1">Closed Tickets</a>
                % if closed == True:
                    <div style="background-color: #008CBA !important; height: 3px;"></div>
                % endif
            </div>
            <div class="right">
                <a href="/newticket?project_id=${project['id']}">New Ticket</a>
            </div>
        </div>
    </div>

    <div class="row">
        <div class="medium-12 columns">
        % if tickets and len(tickets) != 0:
            % for ticket in tickets:
                <div class="box shadow ticket-container">
                    <h5>
                        <div class="bottom-border"><a href="/ticket?ticket_id=${ticket['id']}">${ticket['title']}</a>
                            <div class="small-text indent">#${ticket['number']} opened by <a href="/user?user_id=${user.id}">${ticket['owner']}</a> on ${ticket['created']}</div>
                            % if ticket['closed'] == True:
                                <div class="small-text">Closed <!-- by <a href="/user?user_id=${user.id}">${ticket['owner']}</a>-->on ${ticket['closed_datetime']}</div>
                            % endif
                        </div>
                    </h5>
                    
                    <div class="container-inner">
                        ${ticket['contents'] | n}
                    </div>
                </div>
            % endfor
        % else:
            <div class="box small-light-text">
                There are no tickets for this project yet.
            </div>
        % endif
        </div>
    </div>
    
    <hr/>
