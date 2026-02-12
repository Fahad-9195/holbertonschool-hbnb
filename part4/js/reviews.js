/**
 * HBnB Web Client - Reviews Functions
 * Handles loading and submitting reviews
 */

/**
 * Load reviews for a place
 */
async function loadReviews(placeId) {
    const reviewsContainer = document.getElementById('reviewsContainer');
    const noReviews = document.getElementById('noReviews');
    const reviewsSection = document.getElementById('reviewsSection');

    if (!reviewsContainer || !reviewsSection) return;

    try {
        // Get all reviews and filter by place_id
        const allReviews = await apiRequest('/reviews/');
        const placeReviews = allReviews.filter(review => review.place_id === placeId);

        reviewsSection.classList.remove('hidden');

        if (placeReviews.length === 0) {
            noReviews.classList.remove('hidden');
            reviewsContainer.innerHTML = '';
            return;
        }

        noReviews.classList.add('hidden');

        // Load user information for each review
        const reviewsWithUsers = await Promise.all(
            placeReviews.map(async (review) => {
                try {
                    const user = await apiRequest(`/users/${review.user_id}`);
                    return {
                        ...review,
                        userName: `${user.first_name} ${user.last_name}`,
                    };
                } catch (error) {
                    console.error('Error loading user for review:', error);
                    return {
                        ...review,
                        userName: 'Unknown User',
                    };
                }
            })
        );

        // Display reviews
        // Show edit/delete buttons if user is admin OR if review belongs to current user
        const isUserAdmin = isAdmin();
        const currentUserInfo = getCurrentUserInfo();
        const currentUserId = currentUserInfo ? currentUserInfo.user_id : null;
        
        reviewsContainer.innerHTML = reviewsWithUsers.map(review => {
            // Check if current user owns this review
            const isOwner = currentUserId && review.user_id === currentUserId;
            const canEdit = isUserAdmin || isOwner;
            
            return `
            <div class="review-card" data-review-id="${review.id}" data-review-user-id="${review.user_id}">
                <div class="review-header">
                    <div class="review-author">${escapeHtml(review.userName)}</div>
                    <div style="display: flex; align-items: center; gap: 1rem;">
                        <div class="review-rating">
                            ${generateStars(review.rating)}
                        </div>
                        ${canEdit ? `
                            <div style="display: flex; gap: 0.5rem; margin-left: auto;">
                                <button class="user-action-button-small" onclick="editReview('${review.id}', '${escapeHtml(review.text)}', ${review.rating})" title="Edit Review">Edit</button>
                                <button class="user-action-button-small delete" onclick="deleteReview('${review.id}')" title="Delete Review">Delete</button>
                            </div>
                        ` : ''}
                    </div>
                </div>
                <div class="review-text" id="review-text-${review.id}">${escapeHtml(review.text)}</div>
                <div id="review-edit-form-${review.id}" class="review-edit-form hidden"></div>
            </div>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading reviews:', error);
        reviewsContainer.innerHTML = '<p>Error loading reviews. Please try again later.</p>';
    }
}

/**
 * Delete a review (Admin or owner)
 * Made global for onclick handlers
 */
window.deleteReview = async function(reviewId) {
    if (!confirm('Are you sure you want to delete this review? This action cannot be undone.')) {
        return;
    }

    try {
        await apiRequest(`/reviews/${reviewId}`, {
            method: 'DELETE',
        });

        // Reload reviews
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('id');
        if (placeId) {
            await loadReviews(placeId);
        }
    } catch (error) {
        alert('Error deleting review: ' + (error.message || 'Unknown error'));
        console.error('Error deleting review:', error);
    }
}

/**
 * Edit a review (Admin or owner)
 * Made global for onclick handlers
 */
window.editReview = function(reviewId, currentText, currentRating) {
    const reviewCard = document.querySelector(`[data-review-id="${reviewId}"]`);
    const reviewText = document.getElementById(`review-text-${reviewId}`);
    const editForm = document.getElementById(`review-edit-form-${reviewId}`);
    
    if (!reviewCard || !editForm) return;
    
    // Hide the review text and show edit form
    reviewText.style.display = 'none';
    editForm.classList.remove('hidden');
    
    // Create edit form
    editForm.innerHTML = `
        <div class="review-edit-content">
            <div class="form-group" style="margin-bottom: 1rem;">
                <label for="edit-review-text-${reviewId}" style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem; display: block;">Review Text</label>
                <textarea 
                    id="edit-review-text-${reviewId}" 
                    class="form-control"
                    rows="4"
                    required
                    style="width: 100%; padding: 0.75rem; border: 2px solid var(--border-color); border-radius: var(--border-radius-sm); font-family: var(--font-primary); font-size: 0.95rem; resize: vertical;"
                >${escapeHtml(currentText)}</textarea>
            </div>
            <div class="form-group" style="margin-bottom: 1rem;">
                <label for="edit-review-rating-${reviewId}" style="font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem; display: block;">Rating</label>
                <select id="edit-review-rating-${reviewId}" class="form-control" required style="width: 100%; padding: 0.75rem; border: 2px solid var(--border-color); border-radius: var(--border-radius-sm); font-family: var(--font-primary); font-size: 0.95rem; cursor: pointer;">
                    <option value="1" ${currentRating === 1 ? 'selected' : ''}>1 Star</option>
                    <option value="2" ${currentRating === 2 ? 'selected' : ''}>2 Stars</option>
                    <option value="3" ${currentRating === 3 ? 'selected' : ''}>3 Stars</option>
                    <option value="4" ${currentRating === 4 ? 'selected' : ''}>4 Stars</option>
                    <option value="5" ${currentRating === 5 ? 'selected' : ''}>5 Stars</option>
                </select>
            </div>
            <div style="display: flex; gap: 0.75rem; margin-top: 1.5rem; justify-content: flex-end;">
                <button type="button" class="user-action-button" onclick="cancelEditReview('${reviewId}')" style="background: var(--bg-tertiary); color: var(--text-primary);">Cancel</button>
                <button type="button" class="user-action-button" onclick="saveReview('${reviewId}')" style="background: var(--secondary-color);">Save Changes</button>
            </div>
            <div id="edit-review-error-${reviewId}" class="error-message hidden" style="margin-top: 1rem;"></div>
        </div>
    `;
}

/**
 * Cancel editing a review
 */
window.cancelEditReview = function(reviewId) {
    const reviewText = document.getElementById(`review-text-${reviewId}`);
    const editForm = document.getElementById(`review-edit-form-${reviewId}`);
    
    if (reviewText) reviewText.style.display = 'block';
    if (editForm) {
        editForm.classList.add('hidden');
        editForm.innerHTML = '';
    }
}

/**
 * Save edited review
 */
window.saveReview = async function(reviewId) {
    const reviewText = document.getElementById(`edit-review-text-${reviewId}`).value.trim();
    const reviewRating = document.getElementById(`edit-review-rating-${reviewId}`).value;
    const errorDiv = document.getElementById(`edit-review-error-${reviewId}`);
    
    // Hide previous errors
    if (errorDiv) {
        errorDiv.classList.add('hidden');
        errorDiv.textContent = '';
    }
    
    // Validate
    if (!reviewText) {
        if (errorDiv) {
            errorDiv.textContent = 'Review text is required';
            errorDiv.classList.remove('hidden');
        }
        return;
    }
    
    if (!reviewRating) {
        if (errorDiv) {
            errorDiv.textContent = 'Rating is required';
            errorDiv.classList.remove('hidden');
        }
        return;
    }
    
    try {
        await apiRequest(`/reviews/${reviewId}`, {
            method: 'PUT',
            body: JSON.stringify({
                text: reviewText,
                rating: parseInt(reviewRating),
            }),
        });
        
        // Reload reviews
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('id');
        if (placeId) {
            await loadReviews(placeId);
        }
    } catch (error) {
        if (errorDiv) {
            errorDiv.textContent = error.message || 'Error updating review';
            errorDiv.classList.remove('hidden');
        }
        console.error('Error updating review:', error);
    }
}

/**
 * Handle add review (from place.html)
 */
async function handleAddReview() {
    const addReviewSection = document.getElementById('add-review'); // Task 3 requirement
    const addReviewSectionAlt = document.getElementById('addReviewSection'); // For backward compatibility
    const targetAddReview = addReviewSection || addReviewSectionAlt;
    const placeId = targetAddReview ? targetAddReview.dataset.placeId : null;
    const reviewText = document.getElementById('reviewText').value.trim();
    const reviewRating = document.getElementById('reviewRating').value;

    if (!placeId) {
        showError('reviewFormError', 'Place ID is missing');
        return;
    }

    // Hide previous errors
    hideError('reviewTextError');
    hideError('reviewRatingError');
    hideError('reviewFormError');
    hideSuccess('reviewFormSuccess');

    // Validate inputs
    if (!reviewText) {
        showError('reviewTextError', 'Review text is required');
        return;
    }

    if (!reviewRating) {
        showError('reviewRatingError', 'Rating is required');
        return;
    }

    // Verify place ownership from database before submitting
    // This ensures data integrity and prevents owners from reviewing their own places
    try {
        const place = await apiRequest(`/places/${placeId}`);
        
        // Validate place exists and has owner_id
        if (!place || !place.owner_id) {
            showError('reviewFormError', 'Invalid place. Please refresh the page and try again.');
            const submitButton = document.getElementById('submitReviewButton');
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = 'Submit Review';
            }
            return;
        }
        
        // Get current user ID from token
        const currentUserInfo = getCurrentUserInfo();
        const currentUserId = currentUserInfo ? currentUserInfo.user_id : null;
        
        if (!currentUserId) {
            showError('reviewFormError', 'You must be logged in to submit a review.');
            const submitButton = document.getElementById('submitReviewButton');
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = 'Submit Review';
            }
            return;
        }
        
        // Verify from database: check if current user is the place owner
        // place.owner_id comes directly from the database via API
        if (place.owner_id === currentUserId) {
            showError('reviewFormError', 'You cannot review your own place. Only other users can review your listing.');
            const submitButton = document.getElementById('submitReviewButton');
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = 'Submit Review';
            }
            return;
        }
    } catch (error) {
        // If we can't verify from database, show error
        let errorMessage = 'Could not verify place information. Please try again.';
        if (error.message && error.message.includes('404')) {
            errorMessage = 'Place not found. Please refresh the page and try again.';
        }
        showError('reviewFormError', errorMessage);
        const submitButton = document.getElementById('submitReviewButton');
        if (submitButton) {
            submitButton.disabled = false;
            submitButton.textContent = 'Submit Review';
        }
        return;
    }

    // Disable submit button
    const submitButton = document.getElementById('submitReviewButton');
    submitButton.disabled = true;
    submitButton.textContent = 'Submitting...';

    try {
        await apiRequest('/reviews/', {
            method: 'POST',
            body: JSON.stringify({
                text: reviewText,
                rating: parseInt(reviewRating),
                place_id: placeId,
            }),
        });

        showSuccess('reviewFormSuccess', 'Review submitted successfully!');
        
        // Clear form
        document.getElementById('reviewText').value = '';
        document.getElementById('reviewRating').value = '';

        // Reload reviews
        await loadReviews(placeId);

        // Scroll to reviews section
        const reviewsSection = document.getElementById('reviewsSection');
        if (reviewsSection) {
            reviewsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    } catch (error) {
        showError('reviewFormError', error.message || 'Failed to submit review. Please try again.');
    } finally {
        submitButton.disabled = false;
        submitButton.textContent = 'Submit Review';
    }
}

/**
 * Handle add review from add_review.html form
 */
async function handleAddReviewFromForm() {
    const placeId = document.getElementById('placeId').value.trim();
    const reviewText = document.getElementById('reviewText').value.trim();
    const reviewRating = document.getElementById('reviewRating').value;

    // Hide previous errors
    hideError('placeIdError');
    hideError('reviewTextError');
    hideError('reviewRatingError');
    hideError('formError');
    hideSuccess('formSuccess');

    // Validate inputs
    if (!placeId) {
        showError('placeIdError', 'Place ID is required');
        return;
    }

    if (!reviewText) {
        showError('reviewTextError', 'Review text is required');
        return;
    }

    if (!reviewRating) {
        showError('reviewRatingError', 'Rating is required');
        return;
    }

    // Verify place ownership from database before submitting
    // This ensures data integrity and prevents owners from reviewing their own places
    try {
        const place = await apiRequest(`/places/${placeId}`);
        
        // Validate place exists and has owner_id
        if (!place || !place.owner_id) {
            showError('formError', 'Invalid place. Please check the Place ID and try again.');
            const submitButton = document.getElementById('submitButton');
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = 'Submit Review';
            }
            return;
        }
        
        // Get current user ID from token
        const currentUserInfo = getCurrentUserInfo();
        const currentUserId = currentUserInfo ? currentUserInfo.user_id : null;
        
        if (!currentUserId) {
            showError('formError', 'You must be logged in to submit a review.');
            const submitButton = document.getElementById('submitButton');
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = 'Submit Review';
            }
            return;
        }
        
        // Verify from database: check if current user is the place owner
        // place.owner_id comes directly from the database via API
        if (place.owner_id === currentUserId) {
            showError('formError', 'You cannot review your own place. Only other users can review your listing.');
            const submitButton = document.getElementById('submitButton');
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.textContent = 'Submit Review';
            }
            return;
        }
    } catch (error) {
        // If we can't verify from database, show error
        let errorMessage = 'Could not verify place information. Please try again.';
        if (error.message && error.message.includes('404')) {
            errorMessage = 'Place not found. Please check the Place ID and try again.';
        }
        showError('formError', errorMessage);
        const submitButton = document.getElementById('submitButton');
        if (submitButton) {
            submitButton.disabled = false;
            submitButton.textContent = 'Submit Review';
        }
        return;
    }

    // Disable submit button
    const submitButton = document.getElementById('submitButton');
    submitButton.disabled = true;
    submitButton.textContent = 'Submitting...';

    try {
        await apiRequest('/reviews/', {
            method: 'POST',
            body: JSON.stringify({
                text: reviewText,
                rating: parseInt(reviewRating),
                place_id: placeId,
            }),
        });

        showSuccess('formSuccess', 'Review submitted successfully! Redirecting...');

        // Redirect to place page after short delay
        setTimeout(() => {
            window.location.href = `place.html?id=${placeId}`;
        }, 1500);
    } catch (error) {
        let errorMessage = error.message || 'Failed to submit review. Please try again.';
        // Provide specific message for owner trying to review
        if (errorMessage.includes('cannot review your own place') || errorMessage.includes('own place')) {
            errorMessage = 'You cannot review your own place. Only other users can review your listing.';
        }
        showError('formError', errorMessage);
        submitButton.disabled = false;
        submitButton.textContent = 'Submit Review';
    }
}
