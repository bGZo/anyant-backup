# Anyant Backup

Anyant, unfav/unstar all and storing your data/cookie local.

蚁阅, 取消所有收藏并备份 json+cookie 文件.

## Usage

### Github Actions

Fork and try to config `G_A` & `G_P` & `G_T` in `settings>secerts>actions`. Then it would works weekly well. 😁 

Remember to remove my backup file in `/data/` path.

### Local

2 ways works:

- Clone repo.
- [Recommand] Download `anyant-backup-local.py` & `requirement.txt` file in a new directory. Then try with helpful prompt: 

```shell
$python3 anyant-backup-local.py -h
usage: anyant-backup.py [-h] [-p PASSWORD] account

Anyant Script.

positional arguments:
  account               input your account

optional arguments:
  -h, --help            show this help message and exit
  -p PASSWORD, -password PASSWORD
                        password                                       
```

![image](https://user-images.githubusercontent.com/57313137/169489050-11913d93-5f75-437f-9690-ec1b66ca1c8c.png)


## Notices Your Cookies!

Check followings code whether comment out or not.

If not, Remember remove `config.json`, someone could us cookie do anything. 

Notice don't push cookie on network.

```python
f = open('./data/config.json', 'w')
f.write(json.dumps(backup, ensure_ascii=False)) 
# NOTE: ' to ", via:https://wxnacy.com/2020/05/01/python-print-dict-double-quotation-marks/
f.close()
print('config.json created.')
```
