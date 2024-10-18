// frontend/js/main.js

$(document).ready(function() {
    const API_URL = ''; // Set this to your backend API URL if different

    // Check login status on page load
    checkLoginStatus();

    // Update total points on stat input change
    $('.stat-input').on('input', function() {
        updateTotalPoints();
    });

    function updateTotalPoints() {
        let totalPoints = 0;
        $('.stat-input').each(function() {
            totalPoints += parseInt($(this).val()) || 0;
        });
        $('#total-points').text(totalPoints);
    }

    // Registration Form Submission
    $('#register-form').on('submit', function(e) {
        e.preventDefault();
        const username = $('#register-username').val();
        const password = $('#register-password').val();
        const api_key = $('#register-api-key').val();

        $.ajax({
            url: API_URL + '/register',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ username, password, api_key }),
            success: function(data) {
                showAlert('Registration successful!', 'success');
                $('#register-form')[0].reset();
            },
            error: function(err) {
                showAlert('Error: ' + err.responseJSON.error, 'danger');
            }
        });
    });

    // Login Form Submission
    $('#login-form-element').on('submit', function(e) {
        e.preventDefault();
        const username = $('#login-username').val();
        const password = $('#login-password').val();

        $.ajax({
            url: API_URL + '/login',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ username, password }),
            success: function(data) {
                showAlert('Login successful!', 'success');
                $('#login-form-element')[0].reset();
                checkLoginStatus();
            },
            error: function(err) {
                showAlert('Error: ' + err.responseJSON.error, 'danger');
            }
        });
    });

    // Logout Function
    function logout() {
        $.ajax({
            url: API_URL + '/logout',
            type: 'POST',
            success: function(data) {
                showAlert('Logged out successfully!', 'success');
                checkLoginStatus();
            },
            error: function(err) {
                showAlert('Error: ' + err.responseJSON.error, 'danger');
            }
        });
    }

    // Check Login Status
    function checkLoginStatus() {
        $.ajax({
            url: API_URL + '/get_bots',
            type: 'GET',
            success: function(data) {
                // User is logged in
                $('#auth-forms').hide();
                $('#bot-creator').show();
                $('#bot-list-section').show();
                $('#battle-arena').show();
                $('#auth-links').html(`
                    <li class="nav-item">
                        <a class="nav-link" href="#" id="logout-link">Logout</a>
                    </li>
                `);
                $('#logout-link').on('click', function(e) {
                    e.preventDefault();
                    logout();
                });
                updateBotList();
                updateOpponentBotList();
                updateLeaderboard();
            },
            error: function(err) {
                // User is not logged in
                $('#auth-forms').show();
                $('#bot-creator').hide();
                $('#bot-list-section').hide();
                $('#battle-arena').hide();
                $('#auth-links').html(`
                    <li class="nav-item">
                        <a class="nav-link" href="#" id="register-link">Register</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#" id="login-link">Login</a>
                    </li>
                `);
                $('#register-link').on('click', function(e) {
                    e.preventDefault();
                    $('html, body').animate({
                        scrollTop: $('#registration-form').offset().top
                    }, 500);
                });
                $('#login-link').on('click', function(e) {
                    e.preventDefault();
                    $('html, body').animate({
                        scrollTop: $('#login-form').offset().top
                    }, 500);
                });
                updateLeaderboard();
            }
        });
    }

    // Create Bot
    $('#bot-form').on('submit', function(e) {
        e.preventDefault();
        const name = $('#bot-name').val();
        const stats = {
            'Strength': parseInt($('#strength').val()) || 0,
            'Agility': parseInt($('#agility').val()) || 0,
            'Intelligence': parseInt($('#intelligence').val()) || 0,
            'Defense': parseInt($('#defense').val()) || 0
        };

        // Validate total points
        let totalPoints = 0;
        for (let key in stats) {
            totalPoints += stats[key];
        }
        if (totalPoints > 100) {
            showAlert('Total points allocated exceed 100. Please adjust your stats.', 'danger');
            return;
        }

        $.ajax({
            url: API_URL + '/create_bot',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ name, stats }),
            success: function(data) {
                showAlert('Bot created successfully!', 'success');
                $('#bot-form')[0].reset();
                $('#total-points').text('0');
                updateBotList();
                updateOpponentBotList();
            },
            error: function(err) {
                showAlert('Error: ' + err.responseJSON.error, 'danger');
            }
        });
    });

    // Update User's Bot List
    function updateBotList() {
        $.ajax({
            url: API_URL + '/get_bots',
            type: 'GET',
            success: function(bots) {
                const botList = $('#bot-list');
                const selectBot = $('#select-bot');
                botList.empty();
                selectBot.empty().append('<option value="">Select Your Bot</option>');
                bots.forEach(bot => {
                    botList.append(`<li class="list-group-item">${bot.name} - Wins: ${bot.wins}, Losses: ${bot.losses}</li>`);
                    selectBot.append(`<option value="${bot.id}">${bot.name}</option>`);
                });
            },
            error: function(err) {
                showAlert('Error fetching your bots.', 'danger');
            }
        });
    }

    // Update Opponent Bot List
    function updateOpponentBotList() {
        $.ajax({
            url: API_URL + '/get_leaderboard',
            type: 'GET',
            success: function(bots) {
                const selectOpponentBot = $('#select-opponent-bot');
                selectOpponentBot.empty().append('<option value="">Select Opponent Bot</option>');
                bots.forEach(bot => {
                    selectOpponentBot.append(`<option value="${bot.id}">${bot.name} by ${bot.owner_username}</option>`);
                });
            },
            error: function(err) {
                showAlert('Error fetching opponent bots.', 'danger');
            }
        });
    }

    // Update Leaderboard
    function updateLeaderboard() {
        $.ajax({
            url: API_URL + '/get_leaderboard',
            type: 'GET',
            success: function(leaderboard) {
                const leaderboardBody = $('#leaderboard-body');
                leaderboardBody.empty();
                leaderboard.forEach((bot, index) => {
                    leaderboardBody.append(`
                        <tr>
                            <td>${index + 1}</td>
                            <td>${bot.name}</td>
                            <td>${bot.owner_username}</td>
                            <td>${bot.wins}</td>
                            <td>${bot.losses}</td>
                            <td>${bot.experience}</td>
                        </tr>
                    `);
                });
            },
            error: function(err) {
                showAlert('Error fetching leaderboard.', 'danger');
            }
        });
    }

    // Battle Submission
    $('#battle-form').on('submit', function(e) {
        e.preventDefault();
        const bot_id = $('#select-bot').val();
        const opponent_bot_id = $('#select-opponent-bot').val();
        const prompt = $('#prompt-input').val();

        if (!bot_id || !opponent_bot_id) {
            showAlert('Please select both your bot and an opponent bot.', 'danger');
            return;
        }

        $.ajax({
            url: API_URL + '/battle',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ bot_id, opponent_bot_id, prompt }),
            success: function(data) {
                showAlert(`Battle completed! Winner: ${data.winner}`, 'success');
                $('#battle-winner').text(data.winner);
                $('#user-action').text(data.user_action);
                $('#opponent-action').text(data.opponent_action);
                const battleDetails = $('#battle-details');
                battleDetails.empty();
                for (const [key, value] of Object.entries(data.details)) {
                    battleDetails.append(`<li>${key}: ${value}</li>`);
                }
                $('#battle-results').show();
                updateBotList();
                updateOpponentBotList();
                updateLeaderboard();
            },
            error: function(err) {
                showAlert('Error: ' + err.responseJSON.error, 'danger');
            }
        });
    });

    // Show Alert Function
    function showAlert(message, type) {
        const alertDiv = $(`
            <div class="alert alert-${type} alert-dismissible fade show" role="alert">
                ${message}
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
        `);
        $('#alert-placeholder').append(alertDiv);
        setTimeout(() => {
            alertDiv.alert('close');
        }, 5000);
    }
});
