function changePassword() {
    document.getElementById("passwordForm").style.display = "block";
}

function savePassword() {
    var currentPassword = document.getElementById("currentPassword").value;
    var newPassword = document.getElementById("newPassword").value;
    var confirmPassword = document.getElementById("confirmPassword").value;

    if (newPassword !== confirmPassword) {
        alert("New passwords do not match. Please try again.");
        return;
    }

    // Here you would send the current and new passwords to the server for validation and update.
    // For this example, we'll just log them to the console.
    console.log("Current Password:", currentPassword);
    console.log("New Password:", newPassword);
    console.log("Confirm Password:", confirmPassword);

    // Reset the form and hide it
    document.getElementById("currentPassword").value = "";
    document.getElementById("newPassword").value = "";
    document.getElementById("confirmPassword").value = "";
    document.getElementById("passwordForm").style.display = "none";

    alert("Password changed successfully.");
}
