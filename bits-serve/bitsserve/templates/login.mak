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
            
            // if we find ourselves here, force the user to re-login
            localStorage.clear();

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
                            // save token to local store
                            //localStorage.token = data.token;
                            //localStorage.first = data.user.first;
                            //localStorage.last = data.user.last;
                            //localStorage.email = data.user.email;
                            //localStorage.user_type = data.user.user_type;
                            //localStorage.user_type_description = data.user.user_type_description;

                            // save our token to a cookie, so it gets sent to the server each time
                            var expiration_date = new Date();
                            expiration_date.setFullYear(expiration_date.getFullYear() + 1);
                            document.cookie="token=" + data.token + "; expires=" + expiration_date.toGMTString() + "; path=/";

                            // do redirect
                            window.location.href = "/"

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

