class PetDetailView(generics.RetrieveUpdateDestroyAPIView):
     queryset = Pet.objects.all()
     serializer_class = PetSerializer
     
     def get(self, request, *args, **kwargs):# added by mohsen
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return render(request, 'pet_detail.html', {'serializer': serializer.data})