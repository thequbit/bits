<%inherit file="base.mak"/>

    <ul>
    % if tickets
        % for ticket in tickets
        <li>
            <h3>${ticket['