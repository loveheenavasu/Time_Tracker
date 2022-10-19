

function handlePopupModal(projectId, projectName, projectCategory, createdAt, deadline, department, description){
        const urlFor = `http://${window.location.host}/update_project/${projectId}`
        console.log("data => ",projectId, projectName, projectCategory, createdAt, deadline, department, description);
        let formNode = document.getElementById('projectEditFormModal');
        let projectNameNode = document.getElementById('project-name');
        let projectCategoryNode = document.getElementById('project-category');
        let projectDepartmentNode = document.getElementById('project-department');
        let projectDescriptionNode = document.getElementById('project-description');
        let projectDeadlineNode = document.getElementById('project-deadline');
        let projectStartDateNode = document.getElementById('project-start-date');

        formNode.action = urlFor
        projectNameNode.value = projectName;
        projectCategoryNode.value = projectCategory;
        projectDepartmentNode.value = department;
        projectDescriptionNode.value = description;
        projectDeadlineNode.value = deadline;
        projectStartDateNode.value = createdAt;
    }

   function stopNavigating(event){
        event.preventDefault();
   }


// function apiCalllForForm(id){
//     console.log("Getting form data for user");
//     const url = `http://127.0.0.1:8000/update_project/${id}`
//     fetch(url).then((res) => {
//         console.log("Response form : ", res);
//         let modal = document.getElementById('editProjectModal');
//     }).catch((err) => {
//             console.log("Response form : ", err)
//     })
// }
