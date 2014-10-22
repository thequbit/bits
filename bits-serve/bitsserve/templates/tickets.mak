<%inherit file="base.mak"/>

    <style>
    
        
        div.ticket-container a {
            /*padding-left: 2px;
            padding-top: 4px !important;*/
        }
        
    
    </style>
    
    <div class="row">
        <div class="medium-12 columns bottom-border">
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
            <h5>Tickets</h5>
        </div>
    </div>
    
    <div class="row">
        <div class="medium-12 column">
            <div class="small-text bottom-border">
                Displayed below are all of the tickets for the current project.
                <div class=" normal-text right">
                    <a href="/newticket?project_id=${project['id']}">New Ticket</a>
                </div>
            </div>
            
        </div>
    </div>
    
    <div class="row">
        <div class="medium-12 columns">
        % if tickets and len(tickets) != 0:
            % for ticket in tickets:
                <div class="box shadow ticket-container">
                    <div class="bottom-border"><a href="/ticket?ticket_id=${ticket['id']}">${ticket['title']}</a>
                        <div class="small-text indent">Opened by: ${ticket['owner']} on ${ticket['created']}</div>
                    </div>
                    
                    <div class="container-inner">
                        ${ticket['contents'] | n}
                    </div>
                </div>
            % endfor
        % else:
            <div class="small-light-text">
                There are no tickets for this project yet.
            </div>
        % endif
        </div>
    </div>
