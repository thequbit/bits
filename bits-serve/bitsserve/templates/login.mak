<!doctype html>
<!--[if IE 9]><html class="lt-ie10" lang="en" > <![endif]-->
<html>
<head>

    <link rel="icon" type="image/png" href="static/media/favicon.png">

    <title>bits - Requirements and Ticketing System</title>

    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link href='http://fonts.googleapis.com/css?family=Open+Sans' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" href="static/foundation/css/foundation.css" />

    <style>

        div.login-box {
            width: 300px;
            margin: auto;
            padding: 15px;
        }

    </style>

</head>
<body>

    <div class="row">
        <div class="large-12 columns">
            <h2>bits</h2>
            <hr/>
        </div>
    </div>

    <div class="row">
        <div class="large-12 columns">
            <div class="login-box">
                <h3>Login <small>you must login to continue</small></h3>
                <input placeholder="email" type="text" id="login-email">
                <input placeholder="password" type="password" id="login-password">
                <a href="#" class="small radius button right" id="login-button">Login</a>
            </div>
        </div>
    </div>

    <script src="static/foundation/js/vendor/jquery.js"></script>
    <script src="static/foundation/js/foundation.min.js"></script>
    <script src="static/foundation/js/vendor/modernizr.js"></script>

    <script>
        $(document).foundation();
    </script>

    <script>

        $(document).ready(function() {
            
            // clear our cookie data
            //document.cookie = '';
            
			console.log('cookie:');
			console.log(document.cookie);
			
            $('#login-button').on('click', function(e) {
                email = $('#login-email').val();
                password = $('#login-password').val();
                url = 'authenticate.json?email='+email+'&password='+password;
                console.log('loggin in ...')
                $.ajax({
                    dataType: 'json',
                    url: url,
                    success: function(data) {
                        console.log(data);
                        if ( data.success == true ) {
                            
                            // save our token to a cookie, so it gets sent to the server each time
                            var expiration_date = new Date();
                            expiration_date.setFullYear(expiration_date.getFullYear() + 1);
                            
   							cookie_data = [
								"token=" + data.token + ";",
								"expires=" + expiration_date.toGMTString() + "; ",
								//"path=/; ",
								"domain=" + window.location.hostname + "; "
							].join('');
							
                            console.log('cookie:');
                            console.log(cookie_data);
                            
                            document.cookie = cookie_data;
							//localStorage.setItem('token', token);

                            // do redirect
                            
                            var redirect_url = localStorage.getItem("redirect_url");
                            localStorage.clear();
                            
                            console.log('redirect_url: ' + redirect_url);
                            
                            if ( redirect_url == undefined || redirect_url == null || redirect_url == '' || redirect_url == '/logout' ) {
                                redirect_url = '/';
                            }
                            window.location.href = redirect_url;
                            

                        } else {
                            // TODO: report invalid creds
                            localStorage.clear();
                        }
                    },
                    error: function(data) {
                        // TODO: report error
                        console.log('error on login attempt ...');
                        console.log(data);
                    }
                });
            });
            
        });

    </script>

</body>
</head>

