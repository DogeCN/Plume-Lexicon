#![cfg(test)]

use db::{DBCreator, DBReader};
use rand::distr::{Alphanumeric, SampleString};
use rand::prelude::*;
use rand::rng;
use serialization::{Deserialize, Serialize};
use std::fs;
use std::io::Cursor;

fn create_test_db(db_file: &str, pairs: &[(String, String)]) -> DBCreator<String> {
    let _ = fs::remove_file(db_file);

    let mut db: DBCreator<String> = DBCreator::new(db_file, "name", "名称").unwrap();

    for (key, value) in pairs {
        db.insert(key, value.clone()).unwrap();
    }

    db.export().unwrap();
    db
}

fn test_db(db_file: &str, expected_pairs: &[(String, String)]) {
    let mut reader: DBReader<String> =
        DBReader::from(db_file, format!("{}.values", db_file).as_str()).unwrap();
    reader.load().unwrap();

    assert_eq!(reader.len(), expected_pairs.len());

    for (key, value) in expected_pairs {
        assert!(reader.contains(key));
        assert_eq!(reader.get(key).unwrap(), *value);
    }

    assert!(matches!(reader.get("nonexistentkey"), None));
    assert_eq!(reader.name, "name");
    assert_eq!(reader.name_zh, "名称");

    let _ = fs::remove_file(db_file);
}

#[test]
fn test_serialization() {
    // Test String serialization/deserialization
    let original_string = "Hello, world!".to_string();
    let serialized = dbg!(original_string.serialize());
    let mut cursor = Cursor::new(serialized);
    let deserialized = String::deserialize(&mut cursor).unwrap();
    assert_eq!(original_string, deserialized);

    // Test usize serialization/deserialization
    let original_usize = 234567usize;
    let serialized = dbg!(original_usize.serialize());
    let mut cursor = Cursor::new(serialized);
    let deserialized = usize::deserialize(&mut cursor).unwrap();
    assert_eq!(original_usize, deserialized);

    // Test u32 serialization/deserialization
    let original_u32 = 54321u32;
    let serialized = dbg!(original_u32.serialize());
    let mut cursor = Cursor::new(serialized);
    let deserialized = u32::deserialize(&mut cursor).unwrap();
    assert_eq!(original_u32, deserialized);

    // Test Vec<String> serialization/deserialization
    let original_vec = vec!["one".to_string(), "two".to_string(), "three".to_string()];
    let serialized = dbg!(original_vec.serialize());
    let mut cursor = Cursor::new(serialized);
    let deserialized = Vec::<String>::deserialize(&mut cursor).unwrap();
    assert_eq!(original_vec, deserialized);

    // Test large number serialization
    let large_number = u64::MAX;
    let serialized = dbg!(large_number.serialize());
    let mut cursor = Cursor::new(serialized);
    let deserialized = u64::deserialize(&mut cursor).unwrap();
    assert_eq!(large_number, deserialized);

    // Test empty string serialization
    let empty_string = "".to_string();
    let serialized = dbg!(empty_string.serialize());
    let mut cursor = Cursor::new(serialized);
    let deserialized = String::deserialize(&mut cursor).unwrap();
    assert_eq!(empty_string, deserialized);
}

#[test]
fn test_empty_database() {
    let db_file = "test_empty.db";

    create_test_db(db_file, &[]);

    let mut reader: DBReader<String> =
        DBReader::from(db_file, format!("{}.values", db_file).as_str()).unwrap();
    reader.load().unwrap();

    assert_eq!(reader.len(), 0);
    assert!(reader.keys().is_empty());

    let _ = fs::remove_file(db_file);
}

#[test]
fn test_large_values() {
    let db_file = "test_large.db";

    let large_value = "x".repeat(100 * 1024);

    let pairs = vec![
        ("small_key".to_string(), "small_value".to_string()),
        ("large_key".to_string(), large_value),
    ];

    create_test_db(db_file, &pairs);
    test_db(db_file, &pairs);
}

#[test]
fn test_random_data() {
    let db_file = "test_random.db";

    let mut rng = rng();
    let mut pairs = Vec::new();

    for _ in 0..100 {
        let key_len = rng.random_range(5..20);
        let value_len = rng.random_range(10..1000);

        let key = Alphanumeric.sample_string(&mut rng, key_len);
        let value = Alphanumeric.sample_string(&mut rng, value_len);

        pairs.push((key, value));
    }

    create_test_db(db_file, &pairs);
    test_db(db_file, &pairs);
}

#[test]
fn test_keys_methods() {
    let db_file = "test_keys.db";

    let mut pairs = Vec::new();
    for i in 0..5 {
        pairs.push((format!("key{}", i + 1), format!("value{}", i + 1)));
    }

    create_test_db(db_file, &pairs);

    let mut reader: DBReader<String> =
        DBReader::from(db_file, format!("{}.values", db_file).as_str()).unwrap();
    reader.load().unwrap();
    let keys = reader.keys();

    assert_eq!(keys.len(), pairs.len());

    for (key, _) in pairs {
        assert!(reader.contains(&key));
        assert!(keys.contains(&std::sync::Arc::new(key)));
    }

    let _ = fs::remove_file(db_file);
}
