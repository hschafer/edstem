from edstem import EdCourse, User, Module, Lesson, Slide, QuizQuestion, Challenge
# Getting information about a course
course = EdCourse(1234)  # TODO Auth?

## Get users
users: list[User] = course.get_all_users()
user: User = course.get_user(id or name)  # Error if multiple
# How to unify diff user metadata? Merge in the first call?
# users: list[User2] = course.get_analytics_users()

## Get Sections
tutorials: list[str] = course.get_all_tutorials()

## Get Modules
modules: list[Module] = course.get_all_modules()
module: Module = course.get_module(id or name)
module: Module = Module(id or name)

## Getting Lessons (many ways)
lessons: list[Lesson]  = course.get_all_lessons()
lesson: Lesson = Lesson(id or name)
lesson: Lesson = course.get_lesson(id or name)
lesson: Lesson = module.get_lesson(id or name)

module_lessons: list[Lesson] = module.get_all_lessons()

## Get Slide
slide: Slide = Slide(id)
slide: Slide = course.get_slide(id)
slide: Slide = lesson.get_slide(id or name)

# Get Questions
questions: list[QuizQuestion] = slide.get_questions()
question: QuizQuestion = questions[0]

# Get Challenges
challenges: list[Challenge] = course.get_challenge(id or name?)
challenge_users: list[User] = challenge.get_users()

# Editing Values

## Edit Lessons
lesson.set_name("Foo")
lesson.set_props(dict)
lesson.save()
lesson.delete()  # Delete lesson.
lesson.save()

## Clone Lesson
new_lesson: Lesson = lesson.clone()

## Edit Slide
slide.set_title("foo")
slide.save()

## Edit Questions
question.set_visible(True)
question.save()
question.delete()
question.save()

# Completions

## Lesson Completions
lesson.get_completions(params)

## Challenge Results
lesson.challenge_completions(id or name?, params)
lesson.challenge_completions(params) # Unsure if possible

## Quiz Results
lesson.quiz_completions(id or name?, params)
lesson.quiz_completions(params)) # Unsure if possible

# TBD
## Post Grades
## Connect
## Submit All Challenges
## Submit All Quiz
## Get all Challenge Submissions
## Get all Challenge Submissions for User
## Delete Submission
