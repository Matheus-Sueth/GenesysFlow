import os

pasta = os.listdir('./flows')
pasta.reverse()

for arquivo in pasta:
    flow_file = os.path.abspath(os.path.join('./flows', arquivo))
    cmd = f'archy publish --file "{flow_file}" --clientId 4871996d-fae2-4424-85c7-acda4926395e --clientSecret xcsdtD5Ki_9G4zljaltd2LkyfawUmLIDLTVez0R1MzQ --location sae1.pure.cloud'
    print(flow_file)
    os.system(cmd)