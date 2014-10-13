<%inherit file="base.mak"/>

    <style>
    
        div.ticket-container {
            border-bottom: 1px solid #DDD;
            padding-bottom: 5px;
        }
    
    </style>

    <div>
        <h5>Open Tickets</h5>
        <ul>
        % if tickets:
            % for ticket in tickets:
                % if ticket[1] == False:
                    <div class="ticket-container">
                    <a href="/ticket?ticket_id=${ticket[0]}&project_id=${project_id}">${ticket[16]}</a><br/>
                    <small>Opened by: ${ticket[4]} ${ticket[5]} on ${ticket[3]}</small><br/>
                    </div>
                % endif
            % endfor
        % endif
        </ul>
    </div>
