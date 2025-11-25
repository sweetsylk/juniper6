from recipes.models.user import User

RECIPE_FIXTURES = [{ 
    
    "author": User.objects.first(), 
    "title": "Chicken and Rice",
    "description": "Basic lunch but can be yummy",
    "prep_time": 10,
    "servings": 2,
    "ingredients": "Chicken, Rice",
    "instructions": "Cook rice, cook and season chicken",
    "created_at": "2025-11-16T15:28:00Z",
    "updated_at": "2025-11-17T19:12:00Z"
},{
    "author": User.objects.last(),
    "title": "Chicken Salad",
    "description": "Yummy and healthy",
    "prep_time": 10,
    "servings": 5,
    "ingredients": "Chicken, Lettuce, Tomato",
    "instructions": "Wash chicken, Wash salad, cook and season chicken",
    "created_at": "2025-11-18T10:30:00Z",
    "updated_at": "2025-11-18T19:12:00Z"
},{
    "author": User.objects.order_by('?').first(),
    "title": "Fairy Cakes",
    "description": "Sweet treats everyone will love!",
    "prep_time": 20,
    "servings": 24,
    "ingredients": "Flour, Sugar, Butter, Egg, Milk",
    "instructions": "Whisk sugar and butter together, Add eggs, Add milk, Add Flour",
    "created_at": "2025-10-25T12:00:00Z",
    "updated_at": "2025-10-25T19:00:00Z"
        
},{
    "author": User.objects.order_by('?').last(),
    "title": "Cereal",
    "description": "Good lazy breakfast",
    "prep_time": 5,
    "servings": 1,
    "ingredients": "Coco pops, milk",
    "instructions": "Add milk, add cereal",
    "created_at": "2024-01-12T22:45:16Z",
    "updated_at": "2024-08-01T19:12:22Z"
}]



FOOD_SOURCES = [
    
    "https://cdn.pixabay.com/photo/2017/11/08/22/18/spaghetti-2931846_1280.jpg",
    "https://images.unsplash.com/photo-1609951651556-5334e2706168?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NTB8fGZvb2R8ZW58MHx8MHx8fDA%3D",
    "https://cdn.pixabay.com/photo/2017/05/07/08/56/pancakes-2291908_1280.jpg",
    "https://cdn.pixabay.com/photo/2017/12/10/14/47/pizza-3010062_1280.jpg",
    "https://cdn.pixabay.com/photo/2017/03/30/15/47/churros-2188871_1280.jpg",
    "https://cdn.pixabay.com/photo/2016/01/11/07/18/cupcakes-1133146_1280.jpg",
    "https://cdn.pixabay.com/photo/2014/10/19/20/59/hamburger-494706_1280.jpg",
    "https://cdn.pixabay.com/photo/2016/11/18/15/40/cookies-1835414_1280.jpg",
    "https://cdn.pixabay.com/photo/2015/04/08/13/13/food-712665_1280.jpg",
    "https://cdn.pixabay.com/photo/2024/01/26/23/39/ice-cream-8534875_1280.jpg",
    "https://cdn.pixabay.com/photo/2016/11/19/14/18/oatmeal-1839515_1280.jpg",
    "https://cdn.pixabay.com/photo/2023/05/27/13/49/soup-8021570_1280.jpg",
    "https://cdn.pixabay.com/photo/2016/07/07/19/51/soup-1503117_1280.jpg",
    "https://cdn.pixabay.com/photo/2016/09/21/20/18/pumpkin-soup-1685574_1280.jpg",
    "https://cdn.pixabay.com/photo/2014/04/21/03/02/dumplings-328924_1280.jpg",
    "https://cdn.pixabay.com/photo/2022/07/20/19/11/liver-dumpling-7334775_1280.jpg",

]