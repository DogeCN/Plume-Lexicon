use serialization::Serialize;
use std::{
    fs::{File, remove_file},
    io::{Result, Write, copy},
    marker::PhantomData,
    path::PathBuf,
};
use xz2::write::XzEncoder;

pub struct DBCreator<T> {
    _marker: PhantomData<T>,
    path: PathBuf,
    total: usize,
    count: usize,
    keys: PathBuf,
    values: PathBuf,
    file_key: Option<File>,
    file_values: Option<File>,
    name: String,
    name_zh: String,
}

impl<T: Serialize> DBCreator<T> {
    pub fn new(path: &str, name: &str, name_zh: &str) -> Result<DBCreator<T>> {
        let path = PathBuf::from(path);
        let keys = path.with_extension("keys");
        let values = path.with_extension("values");
        Ok(DBCreator {
            _marker: PhantomData,
            path,
            total: 0,
            count: 0,
            file_key: Some(File::create(&keys)?),
            file_values: Some(File::create(&values)?),
            keys,
            values,
            name: name.to_owned(),
            name_zh: name_zh.to_owned(),
        })
    }

    pub fn insert(&mut self, key: &str, value: impl Into<T>) -> Result<()> {
        let mut buf = Vec::new();
        buf.extend(key.serialize());
        buf.extend(self.total.serialize());
        self.file_key.as_ref().unwrap().write_all(&buf)?;

        let buf = value.into().serialize();
        self.total += buf.len();
        self.file_values.as_ref().unwrap().write_all(&buf)?;
        self.count += 1;
        Ok(())
    }

    pub fn export(&mut self) -> Result<()> {
        let mut encoder = XzEncoder::new(File::create(&self.path)?, 6);
        encoder.write_all(&self.name.serialize())?;
        encoder.write_all(&self.name_zh.serialize())?;
        encoder.write_all(&self.count.serialize())?;
        self.file_key.take();
        self.file_values.take();
        copy(&mut File::open(&self.keys)?, &mut encoder)?;
        copy(&mut File::open(&self.values)?, &mut encoder)?;
        encoder.finish()?;
        remove_file(&self.keys)?;
        remove_file(&self.values)?;
        Ok(())
    }
}
