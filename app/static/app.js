document.addEventListener("DOMContentLoaded", () => {

    function initSortable() {
        var lists = document.querySelectorAll('.task-list');
        lists.forEach(function(list) {
            new Sortable(list, {
                group: 'tasks',
                animation: 150,
                handle: '.drag-handle',
                onEnd: function (evt) {
                    fetch('/api/tasks', {
                        method: 'PATCH',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            'id': evt.item.id,
                            'category': evt.to.id,
                            'category_rank': evt.to.newIndex,
                        })
                    });
                }
            });
        });
    }

    function createTaskCard(rank) {
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

        // Add listener for deleting cards 
        li.querySelector('.delete-btn').addEventListener('click', function () {
            const parent = li.parentElement

            fetch(`/api/tasks?id=${li.id}`, {
                method: 'DELETE',
            });
            li.remove();

            // Update the rank of remaining items
            Array.from(parent.children).forEach((child, index) => {
                fetch(`/api/tasks`, {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        id: child.id,
                        rank: index,
                    }),
                });
            });
        });

        // Add listener for updating card title and body
        li.querySelectorAll('.card-title, .card-body').forEach(field => {
            field.addEventListener('blur', () => {
                fetch('/api/tasks', {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        'id': li.id,
                        'title': `${li.querySelector('.card-title').innerText}`,
                        'body': `${li.querySelector('.card-body').innerText}`
                    })
                })
            });
        });

        // POST the new task
        fetch('/api/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'id': li.id,
                'category': "unsched",
                'category_rank': rank,
                'title': '',
                'body': ''
            })
        });

        return li;
    }

    document.getElementById('add-task-button').addEventListener('click', function() {
        var taskList = document.getElementById('unsched');
        var li = createTaskCard(taskList.children.length);
        taskList.appendChild(li);
    });

    initSortable();
});
