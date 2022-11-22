import argparse
import subprocess
import sys


def sh(command, print_msg=True):
    # run command, print and return output
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = []
    for line in iter(p.stdout.readline, b''):
        line = line.rstrip().decode('utf8')
        if print_msg:
            print(">>>", line)
        lines.append(line.strip()+'\n')
    return lines


def argsParser():
    # get some args
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-w', '--wordlist', type=str, help='wordlist path')
    parser.add_argument('-ul', '--urlfile', type=str, help='target url file')
    args = parser.parse_args()
    if args.urlfile == None or args.wordlist == None:
        parser.print_help()
        sys.exit()
    else:
        return args


def main():
    args = argsParser()
    wordlist = args.wordlist
    url_file = args.urlfile
    result_list = []
    with open(url_file, 'r') as f:
        lines = f.readlines()
        for url in lines:
            if len(url)>4:
                target_url = url.strip()
                run_cmd = f"gobuster dir -z -q -t 50 -k -b 301,302,404,500,501,502 -H 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36' -u {target_url} -w {wordlist}"
                output_lines = sh(command=run_cmd)
                if len(output_lines) > 0:
                    result_list.append('>> '+target_url+'\n')
                    result_list += sh(command=run_cmd)
    if len(result_list) > 0:
        with open('results.txt', 'w') as f:
            f.writelines(result_list)


if __name__ == '__main__':
    main()
