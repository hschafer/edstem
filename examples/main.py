import edstem

DIVIDER = "=" * 20


def main():
    edstem.auth.set_token(".secrets/ed_token")
    course = edstem.EdCourse(38139)

    print(DIVIDER)
    print("Users")
    print(DIVIDER)
    print("Num Users", len(course.get_all_users()))
    print("Example User", course.get_user("Hunter Schafer"))
    print()
    print()

    print(DIVIDER)
    print("Modules")
    print(DIVIDER)
    print("Num Modules", len(course.get_all_modules()))
    print("Example Module", course.get_module("Module 0:  Introduction / Regression"))

    print()
    print()
    print(DIVIDER)
    print("Lessons")
    print(DIVIDER)
    print("Num Lessons", len(course.get_all_lessons()))
    lesson = course.get_lesson("📚 Lecture 0 (March 27): Syllabus + Regression")
    print("Example lesson", lesson)
    module = lesson.get_module()
    print("Example lesson's module", module)


if __name__ == "__main__":
    main()
