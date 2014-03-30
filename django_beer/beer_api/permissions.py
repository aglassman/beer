from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
	"""
	Only allow admin to GET/PUT privileges
	"""

	def has_permission(self, request, view):
		return request.user.is_staff