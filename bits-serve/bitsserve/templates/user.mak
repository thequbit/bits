<%inherit file="base.mak"/>

    <style>

    </style>

    <div class="row">
        <div class="medium-12 columns bottom-border">
            <a href="/">Home</a>
             > 
            <!--<a href="/users">Users</a>--> Users 
             >
            ${user.first} ${user.last}
            <div class="right top-links">
                <a href="/usersettings">${user.first} ${user.last}</a>
            </div>
        </div>
    </div>
    <br/>

    <div class="row">
        <div class="medium-12 columns">
            <h5>${target_user.first} ${target_user.last}</h5>
            <!--
            <div class="box shadow">
                <div class="container-inner">
                    <p></p>
                </div>
            </div>
            -->
        </div>
    </div>
    
    <div class="row">
        <div class="medium-8 columns">
            <div class="row">
                <div class="small-12 columns">
                    % for action in actions:
                        % if action['project_name'] != '':
                            <br/>
                            <h5>${action['project_name']}</h5>
                        % endif
                        <div class="indent">
                            <div class="action-box shadow">
                                <div class="small-light-text">${str(action['created']).split('.')[0]}</div>
                                ${action['contents'] | n}
                            </div>
                        </div>
                    % endfor
                    
                </div>
            </div>
            <hr/>
        </div>
    </div>