document.addEventListener("DOMContentLoaded", () => {
    // Function to initialise sortable lists
    function initSortable() {
        const lists = document.querySelectorAll('.task-list');
        lists.forEach((list) => {
            new Sortable(list, {
                group: 'tasks',
                animation: 150,
                handle: '.drag-handle',
                onEnd: function (evt) {
                    // Handle move within the same list
                    if (evt.to === evt.from) {
                        // Update ranks for all items in the list (reorder only)
                        Array.from(evt.from.children).forEach((child, index) => {
                            fetch(`/api/tasks`, {
                                method: 'PATCH',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({
                                    id: child.id,
                                    category: evt.from.id,
                                    category_rank: index,
                                })
                            })
                        });

                    // Handle move between different lists
                    } else {
                        // Update ranks for items in the original list
                        Array.from(evt.to.children).forEach((child, index) => {
                            fetch(`/api/tasks`, {
                                method: 'PATCH',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({
                                    id: child.id,
                                    category: evt.to.id,
                                    category_rank: index,
                                })
                            }).then((response) => {
                                console.log(response);
                            });
                        });

                        // Update ranks for items in the destination list
                        Array.from(evt.from.children).forEach((child, index) => {
                            fetch(`/api/tasks`, {
                                method: 'PATCH',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({
                                    id: child.id,
                                    category: evt.from.id,
                                    category_rank: index,
                                })
                            })
                        });
                    }
                },
            });
        });
    }

    // Function to add delete event listener
    function addDeleteListener(li) {
        li.querySelector('.delete-btn').addEventListener('click', () => {
            const parent = li.parentElement;

            // DELETE the task
            fetch(`/api/tasks?id=${li.id}`, {
                method: 'DELETE',
            })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error('Failed to delete task');
                    }
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
                                category_rank: index,
                            }),
                        }).catch((error) =>
                            console.error('Error updating rank:', error)
                        );
                    });
                })
                .catch((error) => console.error('Error deleting task:', error));
        });
    }

    // Function to add blur event listener for editing
    function addEditListeners(li) {
        li.querySelectorAll('.card-title, .card-body').forEach((field) => {
            field.addEventListener('blur', () => {
                fetch('/api/tasks', {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        id: li.id,
                        title: li.querySelector('.card-title').innerText,
                        body: li.querySelector('.card-body').innerText,
                    }),
                }).catch((error) => console.error('Error updating task:', error));
            });
        });
    }

    // Function to create a task card
    function createTaskCard(rank) {
        const li = document.createElement('li');
        li.id = Math.floor(Math.random() * 100000);
        li.innerHTML = `
            <div class="drag-handle">
                ⠿
                <button class="delete-btn">✖</button>
            </div>
            <div class="card-title" contenteditable="true" placeholder="Title" spellcheck="false"></div>
            <div class="card-body" contenteditable="true" placeholder="Details" spellcheck="false"></div>
        `;

        // Attach event listeners to the task card
        addDeleteListener(li);
        addEditListeners(li);

        // POST the new task
        fetch('/api/tasks', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                id: li.id,
                category: "unsched",
                category_rank: rank,
                title: '',
                body: '',
            }),
        }).catch((error) => console.error('Error creating task:', error));

        return li;
    }

    // Event listener for adding a new task
    document.getElementById('add-task-button').addEventListener('click', () => {
        const taskList = document.getElementById('unsched');
        const li = createTaskCard(taskList.children.length);
        taskList.appendChild(li);
    });

    // Initialise sortable lists and attach event listeners for pre-existing tasks
    function initialise() {
        document.querySelectorAll('.task-list li').forEach((li) => {
            addDeleteListener(li);
            addEditListeners(li);
        });
        initSortable();
    }

    // Initialise everything on DOMContentLoaded
    initialise();
});
