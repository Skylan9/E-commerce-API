function confirmDelete(event, itemName) {
    const userConfirmed = confirm(`Are you sure you want to delete "${itemName}"?`);
    if (!userConfirmed) {
        event.preventDefault(); // Prevent form submission
    }
}