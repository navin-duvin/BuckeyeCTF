# BuckeyeCTF
Capture the flag event writeup

### PWN category


Dr. staff will see you now

      #include <stdio.h>
      #include <stdlib.h>
      #include <string.h>

      struct Course {
          char name[0x20];
          char instructor[0x20];
          int is_staff;
      };

      static void find_instructor(struct Course *courses, int course_count);
      static void find_course(struct Course *courses, int course_count);
      static void handle_option(int choice, struct Course *courses, int course_count);

      #define NUM_COURSES 50

      int main(int argc, char** argv) {
          struct Course courses[NUM_COURSES];

          setvbuf(stdout, NULL, _IONBF, 0); // turn off buffered output

          FILE *fin = fopen("sp22.txt", "r");
          if (!fin) {
              printf("Failed to open sp22.txt\n");
              return 0;
          }

          // Read in courses and instructors
          int course_count = 0;
          while (course_count < NUM_COURSES) {
              char *s = fgets(courses[course_count].name, 0x20, fin);
              if (!s) break;
              s[strcspn(s, "\n")] = 0; // remove newline

              s = fgets(courses[course_count].instructor, 0x20, fin);
              if (!s) break;
              s[strcspn(s, "\n")] = 0; // remove newline

              courses[course_count].is_staff = 1; // always hide instructors from students until the week before classes
              course_count++;
          }

          while (1) {
              printf("What would you like to do?\n1. Search for a course\n2. Search for an instructor\n> ");
              int choice;
              if (scanf("%d", &choice) != 1) break;
              getc(stdin); // get newline
              handle_option(choice, courses, course_count);
          }
      }

      static void handle_option(int choice, struct Course *courses, int course_count) {
          switch (choice) {
              case 1:
                  find_course(courses, course_count);
                  break;
              case 2:
                  find_instructor(courses, course_count);
                  break;
              default:
                  printf("bad choice\n");
                  break;
          }
      }

      static void find_instructor(struct Course *courses, int course_count) {
          char instructor[0x20];
          char course[0x20];

          printf("What instructor would you like to look up?\n> ");
          char *s = fgets(instructor, 0x20, stdin);
          if (!s) return;
          s[strcspn(s, "\n")] = 0; // remove newline

          if (strcmp(instructor, "Staff") == 0) {
              printf("There were %d results, please be more specific in your search.\n", course_count);
          } else {
              int i;
              for (i=0; i<course_count; i++) {
                  if (strcmp(instructor, courses[i].instructor) == 0) {
                      strncpy(course, courses[i].name, 0x20);
                      break;
                  }
              }
              if (i == course_count) {
                  printf("We couldn't find your instructor.\n");
                  return;
              }
          }

          printf("Professor %s will teach %s, but we'll probably change our minds the week before classes start.\n", instructor, course);
      }




      static void find_course(struct Course *courses, int course_count) {
          char course[0x20];
          char instructor[0x20];

          printf("What course would you like to look up?\n> ");
          char *s = fgets(course, 0x20, stdin);
          if (!s) return;
          s[strcspn(s, "\n")] = 0; // remove newline

          int i;
          for (i=0; i<course_count; i++) {
              if (strcmp(course, courses[i].name) == 0) {
                  strncpy(instructor, courses[i].instructor, 0x20);
                  break;
              }
          }

          if (i == course_count) {
              printf("Sorry, we couldn't find your course.\n");
              return;
          }

          if (courses[i].is_staff) {
              printf("This course will be taught by: Staff\n");
          } else {
              printf("This course will be taught by: %s\n", instructor);
          }

      }


![image](https://user-images.githubusercontent.com/71208443/138666817-ddf87c7c-ad85-4f48-9566-4a48087021e7.png)



ret4win

Try your hand at a tiny ROP chain!

            #include <stdio.h>
            #include <stdlib.h>
            #include <unistd.h>

            __attribute__((constructor)) void ignore_me() {
                setbuf(stdin, NULL);
                setbuf(stdout, NULL);
                setbuf(stderr, NULL);
            }

            void win(int arg0, int arg1, int arg2, int arg3, int arg4, int arg5) {
                char* cmd = "cat flag.txt";
                if (arg0 == 0xdeadbeef && arg1 == 0xcafebabe && arg2 == 0xbeeeeeef &&
                    arg3 == 0x13333337 && arg4 == 0x12345678 && arg5 == 0xabcdefed) {
                    system(cmd);
                }
            }

            void vuln() {
                char buf[32];
                puts("Please leave a message at the tone: **beep**");
                read(0, buf, 32 + 8 + 16);
                close(0);
            }

            int main() {
                vuln();
                return 0;
            }
            
            
![image](https://user-images.githubusercontent.com/71208443/138667877-55801571-9513-4f97-8596-b602b617fa78.png)
