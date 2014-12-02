<%inherit file="base.mak"/>

    <style>
    
    </style>
    
    <div class="row">
        <div class="medium-12 columns bottom-border">
            <a href="/">Home</a>
             >
            <a href="/user?user_id=${user.id}">${user.first} ${user.last}</a>
             > User Settings
            <div class="right top-links">
                <a href="/usersettings">${user.first} ${user.last}</a>
            </div>
        </div>
    </div>
    
    <div class="row">
        <div class="medium-12 columns">
            <h5>User Settings<div class="right small-text"><a href="#" id="save-settings" class="">Save Settings</a></div></h5>
            
        </div>
    </div>
    
    <div class="row">
        <div class="medium-4 columns">
            <div class="box shadow">
                <div class="bottom-border"><h5>General Settings</h5></div>
                <div class="box indent small-light-text">
                    Configure your user settings.
                </div>
                <div class="container-inner">
                    <h6>Website Theme</h6>
                    <div class="indent">
                        <div class="row">
                        
                        % if user.theme == 'light':
                            <div class="small-6 columns"><input type="radio" name="theme" checked></input>Light</div>
                            <div class="small-6 columns"><input type="radio" name="theme"></input>Dark</div>
                        % elif user.theme == 'dark':
                            <div class="small-6 columns"><input type="radio" name="theme"></input>Light</div>
                            <div class="small-6 columns"><input type="radio" name="theme" checked></input>Dark</div>
                        % endif
                        
                        </div>
                    </div>
                </div>
                
            </div>
        </div>
        <div class="medium-4 columns">
            
        </div>
        <div class="medium-4 columns">
            
        </div>
    </div>
 
    <script>
    
        $('#save-settings').on('click', function(e) {
            
            var token = document.cookie.split('=')[1]; 
            var url = '/save_user_settings.json?token=' + token;
            
            var theme = 'light';
            if ( $('input[name=theme]:radio')[1].checked == true ) {
                theme = 'dark';
            }
            
            $.ajax({
                dataType: 'json',
                type: 'POST',
                data: {
                    theme : theme,
                },
                url: url,
                success: function(data) {
                    if( data.success == true ) {
                        console.log('SUCCESS!');
                        window.location.href="/usersettings";
                    }
                },
                error: function(data) {
                    console.log('an error happened while creating task ...');
                    // TODO: report error
                }
            });
           
        });
    
    </script>