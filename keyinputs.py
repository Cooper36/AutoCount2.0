
from pynput.keyboard import Key, Listener
A = input("say hello: ")
print(A)
done =0
print(done)
def show(key):
    
    if key == Key.tab:
        print("good")
          
    if key != Key.tab:
        print("try again")
          
    # by pressing 'delete' button 
    # you can terminate the loop 
    if key == Key.delete: 
        done = 100
        return [False, done]
  
# Collect all event until released
with Listener(on_press = show) as listener:
    listener.join() 

print(done)


