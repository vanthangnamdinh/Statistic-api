# ClickHouse SQLAlchemy Integration

## Tổng quan

File này đã được viết lại để sử dụng SQLAlchemy với ClickHouse thay vì raw queries với `asynch`. 

## Những thay đổi chính:

### 1. Session Management
- Không còn inject session vào constructor
- Sử dụng `ClickHouseSession()` context manager cho mỗi operation
- Tự động rollback khi có lỗi

### 2. Type Safety & Error Handling
- Thêm type hints cho tất cả methods
- Cải thiện error handling với SQLAlchemy exceptions
- Safe value conversion với fallback

### 3. Data Processing
- Sửa bug Boolean check (bool phải check trước int)
- Thêm validation cho datetime
- Safe array processing
- Proper type conversion cho ClickHouse

### 4. Additional Methods
- `find_by_date_range()`: Query theo khoảng thời gian
- `count_by_user_id()`: Đếm số records theo user
- Improved error messages

## Cách sử dụng:

### 1. Cài đặt dependencies:
```bash
poetry add clickhouse-sqlalchemy
```

### 2. Khởi tạo database:
```bash
python -m core.db.init_clickhouse
```

### 3. Sử dụng trong code:
```python
# Repository sẽ tự động được inject thông qua DI container
repo = StatisticLogSQLAlchemyRepo()

# Create log
await repo.create_log(data=log_data)

# Query logs
logs = await repo.find_by_user_id("user123")
count = await repo.count_by_user_id("user123")
```

## Configuration

Đảm bảo trong `config.py` có:
```python
CLICK_HOUSE_HOST: str = "localhost"
CLICK_HOUSE_PORT: int = 9000  
CLICK_HOUSE_DB: str = "statistic"
```

## Lưu ý:

1. **Session Management**: Repository tự quản lý session, không cần inject từ bên ngoài
2. **Error Handling**: Tất cả errors đều được wrap với context message rõ ràng
3. **Type Safety**: Tất cả values đều được validate và convert đúng type
4. **Performance**: Sử dụng connection pooling của SQLAlchemy
5. **Compatibility**: Tương thích với codebase hiện tại thông qua Repository Adapter pattern

## Testing

```python
# Test connection
from core.db.init_clickhouse import check_clickhouse_connection
await check_clickhouse_connection()

# Test repository
repo = StatisticLogSQLAlchemyRepo()
# Test với data mẫu...
```
