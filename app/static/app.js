document.addEventListener("DOMContentLoaded", () => {

    function initSortable() {
        var lists = document.querySelectorAll('.task-list');
        lists.forEach(function(list) {
            new Sortable(list, {
                group: 'tasks',
                animation: 150,
                handle: '.drag-handle',
                onEnd: function (evt) {
                    // Do nothing
                }
            });
        });
    }

    function createTaskCard() {
        var li = document.createElement('li');
        li.id = Math.floor(Math.random() * 100000);
        li.innerHTML = `
            <div class="drag-handle">
                ⠿
                <button class="delete-btn">✖</button>
            </div>
            <div class="card-title" contenteditable="true" placeholder="Title"></div>
            <div class="card-body" contenteditable="true" placeholder="Details"></div>
        `;

        li.querySelector('.delete-btn').addEventListener('click', function () {
            li.remove();
        });
        return li;
    }

    document.getElementById('add-task-button').addEventListener('click', function() {
        var taskList = document.getElementById('unscheduled-tasks');
        var li = createTaskCard();
        taskList.appendChild(li);
    });

    initSortable();
});
