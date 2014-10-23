<%inherit file="base.mak"/>

    % if user and project:

    <style>
    
    </style>
    
    <div class="row">
        <div class="medium-12 columns bottom-border">
            <a href="/">Home</a>
             >
            <a href="/project?project_id=${project['id']}">${project['name']}</a>
             > Settings
            <div class="right top-links">
                <a href="/usersettings">${user.first} ${user.last}</a>
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="medium-12 columns">
            <h5>Project Settings</h5>
            </br>
            <a class="small button round">Save Settings</a>
        </div>
    </div>
    
    <div class="row">
        <div class="medium-4 columns">
            <div class="box shadow">
                <div class="bottom-border"><h5>General Settings</h5></div>
                <div class="box indent small-light-text">
                    Configure your project settings.
                </div>
                <div class="container-inner">
                    <div><input type="checkbox"></input>Enable Project</div>
                </div>
                <div class="box indent small-light-text">
                    Set a completion date for the project.  
                </div>
                <div class="container-inner">
                    <input type="text" placeholder="Due Date"></input>
                </div>
                <div class="box indent small-light-text">
                    Assign this project to a specific customer.
                </div>
                <div class="container-inner">
                    <input type="text" placeholder="Customer Name"></input>
                </div>
            </div>
            <hr/>
        </div>
        <div class="medium-4 columns">
            <div class="box shadow">
                <div class="bottom-border"><h5>Feature Settings</h5></div>
                <div class="box indent small-light-text">
                    Select the features that will be included on the project page for this project.
                </div>
                <div class="container-inner">
                    <div><input type="checkbox"></input>Tasks</div>
                    <div><input type="checkbox"></input>Tickets</div>
                    <div><input type="checkbox"></input>Lists</div>
                    <div><input type="checkbox"></input>Requirements</div>
                    <div><input type="checkbox"></input>Milestones</div>
                    <div><input type="checkbox"></input>Notes</div>
                </div>
            </div>
            <hr/>
        </div>
        <div class="medium-4 columns">
            <div class="box shadow">
                <div class="bottom-border"><h5>Participants</h5></div>
                <div class="box indent small-light-text">
                    Manage the users that have access to this project.
                </div>
                <div class="container-inner">
                    <div><input type="text" placeholder="participant"></input></div>
                    <div class="right">
                        <a href="#">Add User</a>
                    </div>
                    </br>
                </div>
                
            </div>
            <hr/>
        </div>
    </div>
    
    % endif
    