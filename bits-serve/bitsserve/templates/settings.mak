<%inherit file="base.mak"/>

    <style>
    
    </style>
    
    <div class="row">
        <div class="medium-12 columns bottom-border">
            <a href="/">Home</a>
             > System Settings
        </div>
    </div>
    
    <div class="row">
        <div class="medium-12 columns">
            <h5>System Settings<div class="right small-text">
        </div>
    </div>
    
    <div class="row">
        <div class="medium-4 columns">
            <div class="box shadow">
                <div class="bottom-border"><h5>Create User</h5></div>
                <div class="box indent small-light-text">
                    Add a new User
                </div>
                <div class="container-inner">
                    First Name
                    <div class="indent">
                        <input type="text" id="user-first" class="single-input"></input>
                    </div>
                    Last Name
                    <div class="indent">
                        <input type="text" id="user-last" class="single-input"></input>
                    </div>
                    Email Name
                    <div class="indent">
                        <input type="text" id="user-email" class="single-input"></input>
                    </div>
                    Password
                    <div class="indent">
                        <input type="password" id="user-password" class="single-input"></input>
                    </div>
                    <br/>
                    <div class="right">
                        <a href="#" id="create-user">Create</a>
                    </div>
                    <br/>
                </div>
                
            </div>
        </div>
        <div class="medium-4 columns">
            
        </div>
        <div class="medium-4 columns">
            
        </div>
    </div>
 
    <script>
    
        $('#create-user').on('click', function(e) {
            
            var token = document.cookie.split('=')[1]; 
            var url = '/add_user.json?token=' + token;
            
            var first = $('#user-first').val();
            var last = $('#user-last').val();
            var email = $('#user-email').val();
            var password = $('#user-password').val();
            
            $.ajax({
                dataType: 'json',
                type: 'POST',
                data: {
                    organization_id: 1,
                    user_type_id: 1,
                    first: first,
                    last: last,
                    email: email,
                    password: password,
                },
                url: url,
                success: function(data) {
                    if( data.success == true ) {
                        console.log('SUCCESS!');
                        
                        alert('User created successfully.');
                        
                        $('#user-first').val('');
                        $('#user-last').val('');
                        $('#user-email').val('');
                        $('#user-password').val('');
                        
                        window.location.href="/settings";
                    }
                },
                error: function(data) {
                    console.log('an error happened while creating task ...');
                    
                    alert('An error occured while adding the user.');
                    
                    // TODO: report error
                }
            });
           
        });
    
    </script>