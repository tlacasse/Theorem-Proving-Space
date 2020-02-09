import sass
import datetime
import os

def main():
    if not os.path.exists('_build'):
        os.mkdir('_build')
        
    print('REMOVE FILES')
    clear_dir('_build')
    
    print('COMPILE SASS')
    sass.compile(dirname=('sass', '_css'), output_style='compressed')
    
    scripts = [
              'mithril-v2.0.4.min.js'
            , 'plotly.min.js'
            , 'functions.js'
            , 'views/holstepsearch.js'
            , 'views/holstepview.js'
            , 'views/info.js'
            , 'views/mizarsearch.js'
            , 'views/mizarview.js'
            , 'views/navbar.js'
            , 'views/visuals.js'
            , 'root.js'
            ]
    
    styles = [
              '_css/main.css'
            , '_css/search.css'
            , '_css/view.css'
            , '_css/visuals.css'
            ]

    append = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    print('CONCAT SCRIPTS')
    concat_files(scripts, '_build/script_{}.js'.format(append))
    print('CONCAT STYLES')
    concat_files(styles, '_build/style_{}.css'.format(append))

def concat_files(input_list, output):
    with open(output, 'w') as file_out:
        for file_name in input_list:
            print(file_name)
            with open(file_name, 'r') as file_in:
                for line in file_in:
                    file_out.write(line)
            file_out.write('\n')
            
def clear_dir(path):
    for f in os.listdir(path):
        f = path + '/' + f
        print(f)
        os.remove(f)
                
main()
