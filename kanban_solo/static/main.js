$(document).ready(function() {
    document.documentElement.setAttribute('data-theme', localStorage.getItem('kanban_solo_theme'));
});

function changeTheme(theme) {
    if (localStorage.getItem('kanban_solo_theme') == 'default') {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('kanban_solo_theme', 'light');
    } else {
        document.documentElement.setAttribute('data-theme', 'default');
        localStorage.setItem('kanban_solo_theme', 'default');
    }
}

function addSubTask() {
    node = document.getElementById('subtask');
    node.insertAdjacentElement('afterend', node.cloneNode(true));
}